pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Production',
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
                    echo "--- .csproj changes ---" >> report.txt
                    git diff HEAD~1 HEAD -- *.csproj >> report.txt || echo "First commit"
                fi

                if [ -f pom.xml ]; then
                    echo "--- pom.xml changes ---" >> report.txt
                    git diff HEAD~1 HEAD -- pom.xml >> report.txt || echo "First commit"
                fi

                if [ -f build.gradle ]; then
                    echo "--- build.gradle changes ---" >> report.txt
                    git diff HEAD~1 HEAD -- build.gradle >> report.txt || echo "First commit"
                fi
                '''
            }
        }

        stage('Environment Variables Report') {
            steps {
                script {
                    def envReport = new File("env_report.txt")
                    env.each { key, value ->
                        envReport << "${key} = ${value}\n"
                    }
                }
            }
        }

        stage('Publish Reports') {
            steps {
                archiveArtifacts artifacts: 'report.txt, env_report.txt', fingerprint: true
            }
        }
    }
}
