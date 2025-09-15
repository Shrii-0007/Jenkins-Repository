pipeline {
    agent any

    stages {
        stage('Read Config') {
            steps {
                script {
                    // current branch ghe
                    def branchName = env.BRANCH_NAME ?: 'main'

                    // file path ghe
                    def configFile = "appsettings.json"

                    // file read kar
                    def configContent = readJSON file: configFile

                    // values extract kar
                    def appName = configContent.AppSettings.AppName ?: "UnknownApp"
                    def version = configContent.AppSettings.Version ?: "N/A"
                    def environment = configContent.AppSettings.Environment ?: branchName

                    // console madhe show kar
                    echo "✅ Branch: ${branchName}"
                    echo "✅ App: ${appName}"
                    echo "✅ Version: ${version}"
                    echo "✅ Env: ${environment}"

                    // BlueOcean summary sathi
                    currentBuild.description = "App: ${appName} | Ver: ${version} | Env: ${environment}"
                    currentBuild.displayName = "#${BUILD_NUMBER} - ${branchName}"
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
