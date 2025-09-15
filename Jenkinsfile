pipeline {
    agent any

    environment {
        APP_NAME = "MyApplication"

        // Dummy DB URLs
        DEV_DB_URL  = "DUMMY_DEV_DB"
        QA_DB_URL   = "DUMMY_QA_DB"
        UAT_DB_URL  = "DUMMY_UAT_DB"
        PROD_DB_URL = "DUMMY_PROD_DB"

        // Dummy DB credentials (avoid errors)
        DEV_DB_USER  = "dummy_user"
        DEV_DB_PASS  = "dummy_pass"
        QA_DB_USER   = "dummy_user"
        QA_DB_PASS   = "dummy_pass"
        UAT_DB_USER  = "dummy_user"
        UAT_DB_PASS  = "dummy_pass"
        PROD_DB_USER = "dummy_user"
        PROD_DB_PASS = "dummy_pass"
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
                    echo "  🔒 DB Password   : ${dbPass.replaceAll(/./, '*')}" // mask password
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
