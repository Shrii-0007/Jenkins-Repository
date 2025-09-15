pipeline {
    agent any

    stages {
        stage('Checkout Branch') {
            steps {
                script {
                    // Checkout the branch automatically in multibranch pipeline
                    echo "🌿 Running branch: ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Load Branch Config') {
            steps {
                script {
                    // Branch-specific appsettings file
                    def configFile = "appsettings.json" // प्रत्येक branch मध्ये हे file आहे
                    if (!fileExists(configFile)) {
                        error "❌ Config file not found: ${configFile} in branch ${env.BRANCH_NAME}"
                    }

                    def config = readJSON file: configFile

                    // Store values in env for Blue Ocean
                    env.APP_NAME = config.AppSettings.AppName
                    env.VERSION = config.AppSettings.Version
                    env.ENVIRONMENT = config.AppSettings.Environment
                    env.EXTRA_VAR = config.AppSettings.ExtraVar

                    // Print in Blue Ocean logs
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
                    // Add your actual build/deploy commands here
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build Succeeded | Branch: ${env.BRANCH_NAME} | App: ${env.APP_NAME} | Version: ${env.VERSION} | Env: ${env.ENVIRONMENT}"
        }
        failure {
            echo "❌ Build Failed | Branch: ${env.BRANCH_NAME} | App: ${env.APP_NAME} | Version: ${env.VERSION} | Env: ${env.ENVIRONMENT}"
        }
    }
}
