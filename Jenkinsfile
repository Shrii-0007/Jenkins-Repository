pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Branch & Config') {
            steps {
                script {
                    // Current branch
                    def branchName = env.BRANCH_NAME ?: 'main'
                    env.CURRENT_BRANCH = branchName
                    echo "Current Branch: ${branchName}"

                    // Branch-specific appsettings file
                    def configFile = "appsettings.${branchName}.json"

                    if (fileExists(configFile)) {
                        echo "Reading configuration from ${configFile}"
                        def configContent = readFile(configFile)
                        def json = new groovy.json.JsonSlurperClassic().parseText(configContent)

                        // 5 Versions (Shrikant specific)
                        env.SHRIKANT_VERSION1 = json.VERSION1 ?: "Shrikant_1.0.0"
                        env.SHRIKANT_VERSION2 = json.VERSION2 ?: "Shrikant_1.1.0"
                        env.SHRIKANT_VERSION3 = json.VERSION3 ?: "Shrikant_1.2.0"
                        env.SHRIKANT_VERSION4 = json.VERSION4 ?: "Shrikant_1.3.0"
                        env.SHRIKANT_VERSION5 = json.VERSION5 ?: "Shrikant_1.4.0"

                        // 5 Environment Variables (Shrikant specific)
                        env.SHRIKANT_ENV1 = json.ENV1 ?: "Shrikant_DEV_DB"
                        env.SHRIKANT_ENV2 = json.ENV2 ?: "Shrikant_QA_DB"
                        env.SHRIKANT_ENV3 = json.ENV3 ?: "Shrikant_UAT_DB"
                        env.SHRIKANT_ENV4 = json.ENV4 ?: "Shrikant_PROD_DB"
                        env.SHRIKANT_ENV5 = json.ENV5 ?: "Shrikant_FEATURE_FLAG"

                        echo "Versions: ${env.SHRIKANT_VERSION1}, ${env.SHRIKANT_VERSION2}, ${env.SHRIKANT_VERSION3}, ${env.SHRIKANT_VERSION4}, ${env.SHRIKANT_VERSION5}"
                        echo "Environments: ${env.SHRIKANT_ENV1}, ${env.SHRIKANT_ENV2}, ${env.SHRIKANT_ENV3}, ${env.SHRIKANT_ENV4}, ${env.SHRIKANT_ENV5}"
                    } else {
                        echo "⚠ File ${configFile} not found. Using default Shrikant values."
                        env.SHRIKANT_VERSION1 = "Shrikant_1.0.0"
                        env.SHRIKANT_VERSION2 = "Shrikant_1.1.0"
                        env.SHRIKANT_VERSION3 = "Shrikant_1.2.0"
                        env.SHRIKANT_VERSION4 = "Shrikant_1.3.0"
                        env.SHRIKANT_VERSION5 = "Shrikant_1.4.0"
                        env.SHRIKANT_ENV1 = "Shrikant_DEV_DB"
                        env.SHRIKANT_ENV2 = "Shrikant_QA_DB"
                        env.SHRIKANT_ENV3 = "Shrikant_UAT_DB"
                        env.SHRIKANT_ENV4 = "Shrikant_PROD_DB"
                        env.SHRIKANT_ENV5 = "Shrikant_FEATURE_FLAG"
                    }
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                echo "======================================="
                echo "🚀 Deploying Branch: ${env.CURRENT_BRANCH}"
                echo "Application Versions (Shrikant):"
                echo "  V1: ${env.SHRIKANT_VERSION1} | V2: ${env.SHRIKANT_VERSION2} | V3: ${env.SHRIKANT_VERSION3} | V4: ${env.SHRIKANT_VERSION4} | V5: ${env.SHRIKANT_VERSION5}"
                echo "Environment Variables (Shrikant):"
                echo "  ENV1: ${env.SHRIKANT_ENV1} | ENV2: ${env.SHRIKANT_ENV2} | ENV3: ${env.SHRIKANT_ENV3} | ENV4: ${env.SHRIKANT_ENV4} | ENV5: ${env.SHRIKANT_ENV5}"
                echo "======================================="

                // Example .NET build command
                sh '''
                    echo "Starting build for branch $CURRENT_BRANCH..."
                    echo "Versions: $SHRIKANT_VERSION1, $SHRIKANT_VERSION2, $SHRIKANT_VERSION3, $SHRIKANT_VERSION4, $SHRIKANT_VERSION5"
                    echo "Env Vars: $SHRIKANT_ENV1, $SHRIKANT_ENV2, $SHRIKANT_ENV3, $SHRIKANT_ENV4, $SHRIKANT_ENV5"
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
