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
                    writeFile file: 'env_report.html', text: """
                        <html><body><h2>Environment Variables Report</h2><pre>${envText}</pre></body></html>
                    """
                }
            }
        }

        stage('Console Preview of Reports') {
            steps {
                echo "===== DISPLAY: Dependency + Environment Reports ====="
                sh '''
                if [ -f report.txt ]; then cat report.txt; fi
                if [ -f env_report.html ]; then cat env_report.html; fi
                '''
                echo "===== END OF REPORTS ====="
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.txt, env_report.html', fingerprint: true

            // HTML Report Publish
            publishHTML(target: [
                reportDir: '.',
                reportFiles: 'report.txt, env_report.html',
                reportName: "Code & Dependency Reports"
            ])
        }
    }
}
