pipeline {
    agent any

    environment {
        ENV_NAME = "Development"
        BRANCH_NAME = "Development"
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
                set +e
                echo "===== Dependency Change Report =====" > report.txt
                echo "Branch: ${BRANCH_NAME}" >> report.txt
                git log -1 --pretty=format:"%h - %an : %s" >> report.txt
                echo "" >> report.txt

                if [ -f package.json ]; then echo "--- package.json changes ---" >> report.txt; git diff HEAD~1 HEAD -- package.json >> report.txt || echo "First commit"; fi
                if [ -f
