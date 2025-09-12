pipeline {
    agent any

    environment {
        ENV_NAME = "Development"
    }

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
                sh 'echo "Build commands for DEVELOPMENT branch"'
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running unit tests for DEVELOPMENT branch"
                sh 'echo "Unit test commands for DEVELOPMENT branch"'
            }
        }

        stage('Dependency Change Report') {
            steps {
                sh '''
                echo "===== Dependency Change Report =====" > report.txt
                echo "Branch: ${BRANCH_NAME}" >> report.txt
                git log -1 --pretty=format:"%h - %an : %s" >> report.txt
                echo "" >> report.txt

                if [ -f]()
