pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'Github-Credential'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for MAIN branch"
                sh 'echo "Build commands for MAIN branch"'
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running unit tests for MAIN branch"
                sh 'echo "Unit test commands here"'
            }
        }

        stage('Deploy to Production') {
            steps {
                echo "Deploying MAIN branch to PRODUCTION environment..."
                sh 'echo "MAIN branch production deployment commands"'
            }
        }

        stage('Dependency Change Report') {
            steps {
                sh '''
                echo "===== Dependency Change Report =====" > report.txt
                echo "Branch: ${BRANCH_NAME}" >> report.txt
                git log -1 --pretty=format:"%h - %an : %s" >> report.txt
                echo "" >> report.txt

                if [ -f package.json ]; then echo "--- package.json changes ---" >> report.txt; git diff HEAD~1 HEAD -- package.json >> report.txt || echo "First commit"; fi
                if [ -f requirements.txt ];
