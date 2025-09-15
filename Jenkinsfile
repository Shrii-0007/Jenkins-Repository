pipeline {
    agent any

    stages {
        stage('Checkout') {
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

                    // Branch-specific JSON file
                    def configFile = "appsettings.${branch}.json"

                    if (!fileExists(configFile)) {
                        error "❌ Config file not found: ${configFile}"
                    }

                    def config = readJSON file: configFile

                    // Set env variables for Blue Ocean
                    env.APP_NAME = config.AppSettings.AppName
                    env.VERSION  = config.AppSettings.Version
                    env.ENV      = config.AppSettings.Environment
                    env.DB_URL   = config.AppSettings.DB_URL
                    env.EXTRA    = config.AppSettings.ExtraVar

                    echo "✅ Config loaded for branch: ${branch}"
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    echo "======================================="
                    echo "🚀 Deploying Branch: ${env.BRANCH_NAME}"
                    echo "App: ${env.APP_NAME}"
                    echo "Version: ${env.VERSION}"
                    echo "Environment: ${env.ENV}"
                    echo "DB URL: ${env.DB_URL}"
                    echo "Extra Var: ${env.EXTRA}"
                    echo "======================================="

                    // Place your build/deploy commands here
                    sh """
                        echo "Starting deployment for ${env.BRANCH_NAME}"
                        echo "App: $APP_NAME"
                        echo "Version: $VERSION"
                        echo "Environment: $ENV"
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build & Deployment Successful for branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Build Failed for branch: ${env.BRANCH_NAME}"
        }
    }
}
