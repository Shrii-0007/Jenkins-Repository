def SUMMARY = ""  // Global variable for branch summaries

pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
    }
    environment {
        DOTNET_ROOT = "/usr/share/dotnet" // Adjust if needed
    }

    stages {

        stage('Checkout Jenkinsfile') {
            steps {
                echo "🌿 Running pipeline from branch: ${env.BRANCH_NAME}"
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH_NAME}"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: "https://github.com/Shrii-0007/Jenkins-Repository.git",
                        credentialsId: "Github-Credential"
                    ]]
                ])
            }
        }

        stage('Set Branch & Config') {
            steps {
                script {
                    echo "Current Branch: ${env.BRANCH_NAME}"

                    if (fileExists("appsettings.${env.BRANCH_NAME}.json")) {
                        echo "✅ Using config for branch: ${env.BRANCH_NAME}"
                    } else {
                        echo "⚠ File appsettings.${env.BRANCH_NAME}.json not found. Using default Shrikant values."
                    }
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                echo "======================================="
                echo "🚀 Deploying Branch: ${env.BRANCH_NAME}"
                echo "Application Versions (Shrikant):"
                echo "  V1: Shrikant_1.0.0 | V2: Shrikant_1.1.0 | V3: Shrikant_1.2.0 | V4: Shrikant_1.3.0 | V5: Shrikant_1.4.0"
                echo "Environment Variables (Shrikant):"
                echo "  ENV1: Shrikant_DEV_DB | ENV2: Shrikant_QA_DB | ENV3: Shrikant_UAT_DB | ENV4: Shrikant_PROD_DB | ENV5: Shrikant_FEATURE_FLAG"
                echo "======================================="

                sh """
                    echo Starting build for branch ${env.BRANCH_NAME}...
                    echo Versions: Shrikant_1.0.0, Shrikant_1.1.0, Shrikant_1.2.0, Shrikant_1.3.0, Shrikant_1.4.0
                    echo Env Vars: Shrikant_DEV_DB, Shrikant_QA_DB, Shrikant_UAT_DB, Shrikant_PROD_DB, Shrikant_FEATURE_FLAG
                """
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
