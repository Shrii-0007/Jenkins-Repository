pipeline {
    agent any

    environment {
        APP_NAME = "MyDotNetApp"
        BUILD_VERSION = "${env.BUILD_NUMBER}"
        APP_ENV = "Unknown"
        CONFIG_BRANCH = "main"
    }

    options {
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('Checkout Jenkinsfile') {
            steps {
                echo "🌿 Running pipeline from branch: ${env.BRANCH_NAME}"
                checkout scm
            }
        }

        stage('Select Environment Config') {
            steps {
                script {
                    // Branch → Environment mapping
                    def envMap = [
                        "development": "Development",
                        "qa": "QA",
                        "uat": "UAT",
                        "prod": "Production"
                    ]

                    // Loop to find the branch that exists and fetch its appsettings
                    envMap.each { branch, envName ->
                        if (sh(script: "git ls-remote --heads origin ${branch}", returnStatus: true) == 0) {
                            echo "✅ Using branch ${branch} with appsettings.${envName}.json"
                            APP_ENV = envName
                            CONFIG_BRANCH = branch
                        }
                    }

                    echo "ℹ️ Selected environment: ${APP_ENV}"
                    echo "ℹ️ Config branch: ${CONFIG_BRANCH}"

                    // Fetch the appsettings from that branch
                    sh "git fetch origin ${CONFIG_BRANCH}:${CONFIG_BRANCH}"
                    sh "git checkout ${CONFIG_BRANCH} -- appsettings.${APP_ENV}.json"
                    sh "cp -f appsettings.${APP_ENV}.json appsettings.json"
                }
            }
        }

        stage('Check .NET Installation') {
            steps {
                sh 'dotnet --version'
            }
        }

        stage('Restore') {
            steps {
                sh 'dotnet restore'
            }
        }

        stage('Build') {
            steps {
                sh "dotnet build --configuration Release /p:Version=${BUILD_VERSION}"
            }
        }

        stage('Test') {
            steps {
                sh 'dotnet test --no-build --verbosity normal'
            }
        }

        stage('Publish') {
            steps {
                sh 'dotnet publish -c Release -o ./publish_output'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "🚀 Deploying build ${BUILD_VERSION} from main branch with environment: ${APP_ENV}"
                // Add deployment steps here
            }
        }
    }

    post {
        always {
            echo "📊 Branch: ${env.BRANCH_NAME}, App: ${APP_NAME}, Version: ${BUILD_VERSION}, Env: ${APP_ENV}"
        }
        success {
            echo "✅ SUCCESS | Branch: ${env.BRANCH_NAME} | App: ${APP_NAME} | Version: ${BUILD_VERSION} | Env: ${APP_ENV}"
        }
        failure {
            echo "❌ FAILED | Branch: ${env.BRANCH_NAME} | App: ${APP_NAME} | Version: ${BUILD_VERSION} | Env: ${APP_ENV}"
        }
    }
}
