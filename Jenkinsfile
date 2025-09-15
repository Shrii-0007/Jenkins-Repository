pipeline {
    agent any
    environment {
        APP_NAME = "MyDotNetApp"
        VERSION = "1.0.${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    echo "✅ SUCCESS | Branch: ${env.BRANCH_NAME} | App: ${APP_NAME} | Version: ${VERSION}"
                }
            }
        }

        stage('Select Config') {
            steps {
                script {
                    def configFile = ""
                    if (env.BRANCH_NAME == "development") {
                        configFile = "appsettings.Development.json"
                    } else if (env.BRANCH_NAME == "qa") {
                        configFile = "appsettings.QA.json"
                    } else if (env.BRANCH_NAME == "uat") {
                        configFile = "appsettings.UAT.json"
                    } else if (env.BRANCH_NAME == "prod") {
                        configFile = "appsettings.Prod.json"
                    } else {
                        configFile = "appsettings.Development.json"
                    }

                    echo "Using config file: ${configFile}"
                }
            }
        }

        stage('Build') {
            steps {
                sh 'dotnet restore'
                sh 'dotnet build --configuration Release'
            }
        }

        stage('Publish') {
            steps {
                sh 'dotnet publish -c Release -o out'
            }
        }
    }
    post {
        success {
            echo "🎉 Build Success | Branch: ${env.BRANCH_NAME} | App: ${APP_NAME} | Version: ${VERSION}"
        }
        failure {
            echo "❌ Build Failed | Branch: ${env.BRANCH_NAME} | App: ${APP_NAME}"
        }
    }
}
