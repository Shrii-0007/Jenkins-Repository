pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'UAT',
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'Github-Credential'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for UAT branch"
                sh 'echo "Build commands for UAT branch"'
            }
        }

        stage('Deploy to UAT') {
            steps {
                echo "Deploying to UAT environment..."
                sh 'echo "UAT deployment commands"'
            }
        }

        stage('Publish Report') {
            steps {
                sh 'echo "UAT branch report" > report.txt'
                archiveArtifacts artifacts: 'report.txt', fingerprint: true
            }
        }
    }
}
