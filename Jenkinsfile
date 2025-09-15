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
                    // Branch-specific JSON
                    def configFile = ''
                    switch(env.BRANCH_NAME.toLowerCase()) {
                        case 'development': configFile = 'appsettings.Development.json'; break
                        case 'qa':          configFile = 'appsettings.QA.json'; break
                        case 'uat':         configFile = 'appsettings.UAT.json'; break
                        case 'prod':        configFile = 'appsettings.Production.json'; break
                        default:            configFile = 'appsettings.json'
                    }

                    echo "Reading config from file: ${configFile}"

                    // Read JSON using Pipeline Utility Steps plugin
                    def jsonContent = readJSON file: configFile

                    // Set env vars from JSON
                    env.APP_NAME  = jsonContent.AppSettings.AppName
                    env.VERSION   = jsonContent.AppSettings.Version
                    env.ENV_NAME  = jsonContent.AppSettings.Environment
                    env.DB_URL    = jsonContent.AppSettings.DB_URL
                    env.EXTRA_VAR = jsonContent.AppSettings.ExtraVar

                    // Display on Blue Ocean / Console
                    echo "🌿 Branch      : ${env.BRANCH_NAME}"
                    echo "🚀 App Name    : ${env.APP_NAME}"
                    echo "⚡ Version     : ${env.VERSION}"
                    echo "💾 DB URL      : ${env.DB_URL}"
                    echo "💡 Extra Var   : ${env.EXTRA_VAR}"
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    echo "======================================="
                    echo "  🚀 Deploying Application"
                    echo "  Branch      : ${env.BRANCH_NAME}"
                    echo "  Application : ${env.APP_NAME}"
                    echo "  Version     : ${env.VERSION}"
                    echo "  Environment : ${env.ENV_NAME}"
                    echo "  DB URL      : ${env.DB_URL}"
                    echo "======================================="

                    // Example shell command for deployment
                    sh '''
                        echo "Deploying ${APP_NAME} version ${VERSION} to ${ENV_NAME}"
                        echo "Connecting to DB: ${DB_URL}"
                    '''
                }
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
