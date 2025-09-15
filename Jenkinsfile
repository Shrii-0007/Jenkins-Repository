pipeline {
    agent any

    stages {
        stage('Checkout Current Branch') {
            steps {
                script {
                    echo "🌿 Running branch: ${env.BRANCH_NAME}"

                    // Checkout सध्याचा branch (dev/qa/uat/prod)
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${env.BRANCH_NAME}"]],
                        userRemoteConfigs: [[
                            url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                            credentialsId: 'Github-Credential'
                        ]]
                    ])
                }
            }
        }

        stage('Load Config') {
            steps {
                script {
                    def configFile = "appsettings.json"

                    if (!fileExists(configFile)) {
                        error "❌ ${configFile} not found in branch ${env.BRANCH_NAME}"
                    }

                    // Read branch specific appsettings.json
                    def config = readJSON file: configFile

                    env.APP_NAME    = config.AppSettings.AppName
                    env.VERSION     = config.AppSettings.Version
                    env.ENVIRONMENT = config.AppSettings.Environment

                    echo "📂 Loaded Config from ${env.BRANCH_NAME}"
                    echo "   📝 AppName    : ${env.APP_NAME}"
                    echo "   📝 Version    : ${env.VERSION}"
                    echo "   📝 Environment: ${env.ENVIRONMENT}"
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    echo "🚀 Starting Build & Deploy"
                    // इथे actual build/deploy commands टाकायच्या
                }
            }
        }
    }

    post {
        success {
            echo "✅ SUCCESS | Branch: ${env.BRANCH_NAME} | App: ${env.APP_NAME} | Version: ${env.VERSION} | Env: ${env.ENVIRONMENT}"
        }
        failure {
            echo "❌ FAILED | Branch: ${env.BRANCH_NAME}"
        }
    }
}
