pipeline {
    agent any

    environment {
        ENV_NAME = "Development"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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
                echo "Branch: ${env.BRANCH_NAME}" >> report.txt
                git log -1 --pretty=format:"%h - %an : %s" >> report.txt
                echo "" >> report.txt

                if [ -f package.json ]; then echo "--- package.json changes ---" >> report.txt; git diff HEAD~1 HEAD -- package.json >> report.txt || echo "First commit"; fi
                if [ -f requirements.txt ]; then echo "--- requirements.txt changes ---" >> report.txt; git diff HEAD~1 HEAD -- requirements.txt >> report.txt || echo "First commit"; fi
                if ls *.csproj 1> /dev/null 2>&1; then echo "--- .csproj changes ---" >> report.txt; git diff HEAD~1 HEAD -- *.csproj >> report.txt || echo "First commit"; fi
                if [ -f pom.xml ]; then echo "--- pom.xml changes ---" >> report.txt; git diff HEAD~1 HEAD -- pom.xml >> report.txt || echo "First commit"; fi
                if [ -f build.gradle ]; then echo "--- build.gradle changes ---" >> report.txt; git diff HEAD~1 HEAD -- build.gradle >> report.txt || echo "First commit"; fi
                '''
            }
        }

        stage('Environment Variables Report') {
            steps {
                script {
                    def envText = ""
                    env.each { key, value -> envText += "${key} = ${value}\n" }
                    writeFile file: 'env_report.txt', text: envText
                }
            }
        }

        stage('Console Preview of Reports') {
            steps {
                echo "===== DISPLAY: Dependency + Environment Reports ====="
                sh '''
                if [ -f report.txt ]; then cat report.txt; fi
                if [ -f env_report.txt ]; then cat env_report.txt; fi
                '''
                echo "===== END OF REPORTS ====="
            }
        }

        stage('Publish Reports') {
            steps {
                archiveArtifacts artifacts: 'report.txt, env_report.txt', fingerprint: true
            }
        }
    }
}
