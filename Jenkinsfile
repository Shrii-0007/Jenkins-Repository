pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Read Branch Config') {
            steps {
                script {
                    // Current branch
                    def branch = env.BRANCH_NAME
                    echo "🌿 Current branch: ${branch}"

                    // Branch-specific config file
                    def configFile = "appsettings.json" // प्रत्येक branch मध्ये same file आहे
                    if (!fileExists(configFile)) {
                        error "❌ Config file not found: ${configFile}"
                    }

                    // Read JSON
                    def config = readJSON file: configFile

                    // Store values in environment variables for Blue Ocean
                    env.APP_NAME = config.AppSettings.AppName
                    env.VERSION = config.AppSettings.Version
                    env.ENVIRONMENT = config.AppSettings.Environment
                    env.EXTRA_VAR = config.AppSettings.ExtraVar

                    // Print for logs / Blue Ocean
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
                    echo "🚀 Build & Deploy logic goes here for branch: ${env.BRANCH_NAME}"
                    // Your build/deploy commands
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build Succeeded for branch: ${env.BRANCH_NAME} | Version: ${env.VERSION} | Environment: ${env.ENVIRONMENT}"
        }
        failure {
            echo "❌ Build Failed for branch: ${env.BRANCH_NAME}"
        }
    }
}
