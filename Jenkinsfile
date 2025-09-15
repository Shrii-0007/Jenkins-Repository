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

        stage('Setup .NET SDK') {
            steps {
                sh '''
                    echo "📥 Installing .NET SDK..."
                    wget https://dotnet.microsoft.com/download/dotnet/scripts/v1/dotnet-install.sh -O dotnet-install.sh
                    chmod +x dotnet-install.sh
                    ./dotnet-install.sh --channel 8.0 --install-dir $HOME/dotnet
                    export PATH=$PATH:$HOME/dotnet
                    dotnet --version
                '''
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
                    echo "📂 Using config file: ${configFile}"
                }
            }
        }

        stage('Build') {
            steps {
                sh '''
                    export PATH=$PATH:$HOME/dotnet
                    dotnet restore
                    dotnet build --configuration Release
                '''
            }
        }

        stage('Publish') {
            steps {
                sh '''
                    export PATH=$PATH:$HOME/dotnet
                    dotnet publish -c Release -o out
                '''
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
