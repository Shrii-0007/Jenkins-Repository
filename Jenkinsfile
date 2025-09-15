pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    echo "🌿 Current branch: ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Load Config') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'main') {
                        echo "ℹ️ Skipping config load for main branch (no appsettings.json expected)"
                        env.APP_NAME    = "MainBranch"
                        env.VERSION     = "N/A"
                        env.ENVIRONMENT = "N/A"
                    } else {
                        def configFile = "appsettings.json"
                        if (!fileExists(configFile)) {
                            error "❌ ${configFile} not found in branch ${env.BRANCH_NAME}"
                        }

                        def config = readJSON file: configFile
                        env.APP_NAME    = config.AppSettings.AppName
                        env.VERSION     = config.AppSettings.Version
                        env.ENVIRONMENT = config.AppSettings.Environment

                        echo "📂 Config loaded from branch: ${env.BRANCH_NAME}"
                        echo "   📝 AppName    : ${env.APP_NAME}"
                        echo "   📝 Version    : ${env.VERSION}"
                        echo "   📝 Environment: ${env.ENVIRONMENT}"
                    }
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                echo "🚀 Build & Deploy for ${env.BRANCH_NAME} | ${env.APP_NAME} | ${env.VERSION} | ${env.ENVIRONMENT}"
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
