pipeline {
    agent any

    environment {
        // Default values (optional, can be overridden by branch-specific config)
        APP_NAME = 'UnknownApp'
        VERSION = '0.0-Unknown'
        ENVIRONMENT = 'Unknown'
        EXTRA_VAR = 'N/A'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    echo "🌿 Checking out branch: ${env.BRANCH_NAME}"
                    checkout([$class: 'GitSCM',
                        branches: [[name: "${env.BRANCH_NAME}"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'Github-Credential',
                            url: 'https://github.com/Shrii-0007/Jenkins-Repository.git'
                        ]]
                    ])
                }
            }
        }

        stage('Load Branch Config') {
            steps {
                script {
                    def configFile = "appsettings.json" // प्रत्येक branch मध्ये same file आहे

                    if (!fileExists(configFile)) {
                        error "❌ Config file not found: ${configFile} in branch ${env.BRANCH_NAME}"
                    }

                    def config = readJSON file: configFile

                    env.APP_NAME = config.AppSettings.AppName
                    env.VERSION = config.AppSettings.Version
                    env.ENVIRONMENT = config.AppSettings.Environment
                    env.EXTRA_VAR = config.AppSettings.ExtraVar

                    echo "📝 AppName: ${env.APP_NAME}"
                    echo "📝 Version: ${env.VERSION}"
                    echo "📝 Environment: ${env.ENVIRONMENT}"
                    echo "📝 ExtraVar: ${env.EXTRA_VAR}"
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    echo "🚀 Running Build & Deploy for branch: ${env.BRANCH_NAME}"
                    // इथे तुमचे real build/deploy commands ठेवा
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build Succeeded | Branch: ${env.BRANCH_NAME} | Version: ${env.VERSION} | Environment: ${env.ENVIRONMENT}"
        }
        failure {
            echo "❌ Build Failed | Branch: ${env.BRANCH_NAME} | Version: ${env.VERSION} | Environment: ${env.ENVIRONMENT}"
        }
        always {
            // Blue Ocean dashboard मध्ये display साठी
            echo "📊 Branch: ${env.BRANCH_NAME}, App: ${env.APP_NAME}, Version: ${env.VERSION}, Env: ${env.ENVIRONMENT}"
        }
    }
}
