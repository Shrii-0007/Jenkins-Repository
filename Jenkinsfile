pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Development',
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'Github-Credential'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for DEVELOPMENT branch"
                sh 'echo "Build commands for development branch"'
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running unit tests for DEVELOPMENT branch"
                sh 'echo "Unit test commands here"'
            }
        }

        stage('Publish Report') {
            steps {
                sh 'echo "Development branch report" > report.txt'
                archiveArtifacts artifacts: 'report.txt', fingerprint: true
            }
        }
    }
}
