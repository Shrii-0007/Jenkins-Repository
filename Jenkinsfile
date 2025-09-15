pipeline {
    agent any

    stages {
        stage('Checkout Branch') {
            steps {
                script {
                    checkout scm
                    echo "✅ Checked out branch: ${env.BRANCH_NAME}"
                }
            }
        }

        stage('Read Config') {
            steps {
                script {
                    def configFile = "appsettings.json"

                    if (env.BRANCH_NAME == "main") {
                        echo "ℹ️ Skipping config load for main branch"
                        currentBuild.description = "Main branch - Jenkinsfile only"
                        currentBuild.displayName = "#${BUILD_NUMBER} - main"
                    } else if (fileExists(configFile)) {
                        def configContent = readJSON file: configFile
                        def appName = configContent.AppSettings.AppName ?: "UnknownApp"
                        def version = configContent.AppSettings.Version ?: "N/A"
                        def environment = configContent.AppSettings.Environment ?: env.BRANCH_NAME

                        echo "✅ Branch: ${env.BRANCH_NAME}"
                        echo "✅ App: ${appName}"
                        echo "✅ Version: ${version}"
                        echo "✅ Env: ${environment}"

                        currentBuild.description = "App: ${appName} | Ver: ${version} | Env: ${environment}"
                        currentBuild.displayName = "#${BUILD_NUMBER} - ${env.BRANCH_NAME}"
                    } else {
                        error "❌ Config file not found in branch: ${env.BRANCH_NAME}"
                    }
                }
            }
        }

        stage('Build') {
            steps {
                echo "🚀 Building ${env.BRANCH_NAME} branch..."
            }
        }
    }

    post {
        success {
            echo "✅ SUCCESS | Branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ FAILED | Branch: ${env.BRANCH_NAME}"
        }
    }
}
