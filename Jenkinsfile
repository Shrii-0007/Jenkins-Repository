pipeline {
    agent any

    environment {
        APP_NAME = "MyApplication"
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

                    // Save version to file for artifact
                    writeFile file: 'version.txt', text: "App: ${APP_NAME}\nVersion: ${env.VERSION}\nEnvironment: Development"
                }
            }
        }

        stage('Development') {
            steps {
                echo "======================================="
                echo "  🚀 Deploying to Development"
                echo "  Application : ${env.APP_NAME}"
                echo "  Version     : ${env.VERSION}"
                echo "======================================="

                sh '''
                    echo "Starting Development Deployment..."
                    echo "App: $APP_NAME"
                    echo "Version: $VERSION"
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
