pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'QA',
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'Github-Credential'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for QA branch"
                sh 'echo "Build commands for QA branch"'
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running unit tests for QA branch"
                sh 'echo "Unit test commands for QA"'
            }
        }

        stage('Deploy to QA') {
            steps {
                echo "Deploying to QA environment..."
                sh 'echo "QA deployment commands"'
            }
        }

        stage('Publish Report') {
            steps {
                sh 'echo "QA branch report" > report.txt'
                archiveArtifacts artifacts: 'report.txt', fingerprint: true
            }
        }
    }
}
