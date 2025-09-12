pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Production',
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'github-credentials'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for PRODUCTION branch"
                sh 'echo "Build commands for Production branch"'
            }
        }

        stage('Deploy to Production') {
            steps {
                echo "Deploying to Production environment..."
                sh 'echo "Production deployment commands"'
            }
        }

        stage('Publish Report') {
            steps {
                sh 'echo "Production branch report" > report.txt'
                archiveArtifacts artifacts: 'report.txt', fingerprint: true
            }
        }
    }
}
