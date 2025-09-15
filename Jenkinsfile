pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Read .NET Config') {
            steps {
                script {
                    def configFile = ''
                    switch(env.BRANCH_NAME.toLowerCase()) {
                        case 'dev':     configFile = 'appsettings.Development.json'; break
                        case 'qa':      configFile = 'appsettings.QA.json'; break
                        case 'uat':     configFile = 'appsettings.UAT.json'; break
                        case 'staging': configFile = 'appsettings.Staging.json'; break
                        case 'prod':    configFile = 'appsettings.Production.json'; break
                        default:        configFile = 'appsettings.json'
                    }

                    // Read JSON content (requires Pipeline Utility Steps plugin)
                    def jsonContent = readJSON file: configFile

                    env.APP_NAME  = jsonContent.AppSettings.AppName
                    env.VERSION   = jsonContent.AppSettings.Version
                    env.ENV_NAME  = jsonContent.AppSettings.Environment
                    env.DB_URL    = jsonContent.AppSettings.DB_URL
                    env.EXTRA_VAR = jsonContent.AppSettings.ExtraVar

                    echo "======================================="
                    echo "🌿 Branch      : ${env.BRANCH_NAME}"
                    echo "🚀 App         : ${env.APP_NAME}"
                    echo "⚡ Version     : ${env.VERSION}"
                    echo "💾 DB URL      : ${env.DB_URL}"
                    echo "💡 Extra Var   : ${env.EXTRA_VAR}"
                    echo "======================================="
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                echo "🔨 Building and Deploying branch: ${env.BRANCH_NAME}"
                sh '''
                    echo "App: $APP_NAME"
                    echo "Version: $VERSION"
                    echo "Branch: $BRANCH_NAME"
                    echo "Env Var: $EXTRA_VAR"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build & Deployment Successful!"
        }
        failure {
            echo "❌ Build Failed!"
        }
    }
}
