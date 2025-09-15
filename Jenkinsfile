pipeline {
    agent any

    environment {
        APP_NAME = "MyApplication"

        // Dummy DB URLs for now (replace with real DB URLs later)
        DEV_DB_URL  = "DUMMY_DEV_DB"
        QA_DB_URL   = "DUMMY_QA_DB"
        UAT_DB_URL  = "DUMMY_UAT_DB"
        PROD_DB_URL = "DUMMY_PROD_DB"

        // Optional: Jenkins credentials for future secure DB access
        DEV_DB_USER  = credentials('dev-db-username')
        DEV_DB_PASS  = credentials('dev-db-password')
        QA_DB_USER   = credentials('qa-db-username')
        QA_DB_PASS   = credentials('qa-db-password')
        UAT_DB_USER  = credentials('uat-db-username')
        UAT_DB_PASS  = credentials('uat-db-password')
        PROD_DB_USER = credentials('prod-db-username')
        PROD_DB_PASS = credentials('prod-db-password')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Version') {
            steps {
                script {
                    def commitHash = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.VERSION = "${BUILD_NUMBER}-${commitHash}"
                    
                    writeFile file: 'version.txt', text: """App: ${APP_NAME}
Version: ${env.VERSION}
Branch: ${env.BRANCH_NAME}"""
                }
            }
        }

        stage('Show Environment Variables') {
            steps {
                script {
                    def dbUrl = ""
                    def dbUser = ""
                    def dbPass = ""

                    switch(env.BRANCH_NAME) {
                        case 'dev':
                            dbUrl = DEV_DB_URL
                            dbUser = DEV_DB_USER
                            dbPass = DEV_DB_PASS
                            break
                        case 'qa':
                            dbUrl = QA_DB_URL
                            dbUser = QA_DB_USER
                            dbPass = QA_DB_PASS
                            break
                        case 'uat':
                            dbUrl = UAT_DB_URL
                            dbUser = UAT_DB_USER
                            dbPass = UAT_DB_PASS
                            break
                        case 'prod':
                            dbUrl = PROD_DB_URL
                            dbUser = PROD_DB_USER
                            dbPass = PROD_DB_PASS
                            break
                        default:
                            dbUrl = "No DB Config"
                            dbUser = "N/A"
                            dbPass = "N/A"
                    }

                    echo "======================================="
                    echo "  🌿 Branch        : ${env.BRANCH_NAME}"
                    echo "  💾 DB URL        : ${dbUrl}"
                    echo "  👤 DB User       : ${dbUser}"
                    echo "  🔒 DB Password   : ${dbPass.replaceAll(/./, '*')}"
                    echo "  🚀 App Version   : ${env.VERSION}"
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
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build & Deployment Successful!"
            archiveArtifacts artifacts: 'version.txt', fingerprint: true
        }
        failure {
            echo "❌ Build Failed!"
        }
    }
}
