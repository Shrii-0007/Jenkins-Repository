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
                sh 'echo "Build commands for Main branch"'
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
                echo "Deploying MAIN branch to Production environment..."
                sh 'echo "Production deployment commands"'
            }
        }

        stage('Dependency Change Report') {
            steps {
                sh '''
                echo "===== Dependency Change Report =====" > report.txt
                echo "Branch: ${BRANCH_NAME}" >> report.txt
                echo "Commit Info:" >> report.txt
                git log -1 --pretty=format:"%h - %an : %s" >> report.txt
                echo "" >> report.txt

                if [ -f package.json ]; then
                    echo "--- package.json changes ---" >> report.txt
                    git diff HEAD~1 HEAD -- package.json >> report.txt || echo "First commit"
                fi

                if [ -f requirements.txt ]; then
                    echo "--- requirements.txt changes ---" >> report.txt
                    git diff HEAD~1 HEAD -- requirements.txt >> report.txt || echo "First commit"
                fi

                if ls *.csproj 1> /dev/null 2>&1; then
                    echo "--- .cs
