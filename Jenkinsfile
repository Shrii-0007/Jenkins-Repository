pipeline {
    agent any

    environment {
        ENV_NAME = "Development"
        BRANCH_NAME = "Development"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${BRANCH_NAME}",
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'Github-Credential'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for ${BRANCH_NAME} branch"
                sh 'echo "Build commands for ${BRANCH_NAME}"'
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running unit tests for ${BRANCH_NAME} branch"
                sh 'echo "Unit test commands for ${BRANCH_NAME}"'
            }
        }

        stage('Generate Dashboard Report') {
            steps {
                script {
                    // Collect commit info
                    def commitInfo = sh(script: "git log -1 --pretty=format:'%h - %an : %s'", returnStdout: true).trim()

                    // Collect dependency changes
                    def depReport = ""
                    depReport += sh(script: "[ -f package.json ] && git diff HEAD~1 HEAD -- package.json || echo ''", returnStdout: true)
                    depReport += sh(script: "[ -f requirements.txt ] && git diff HEAD~1 HEAD -- requirements.txt || echo ''", returnStdout: true)
                    depReport += sh(script: "ls *.csproj 1>/dev/null 2>&1 && git diff HEAD~1 HEAD -- *.csproj || echo ''", returnStdout: true)
                    depReport += sh(script: "[ -f pom.xml ] && git diff HEAD~1 HEAD -- pom.xml || echo ''", returnStdout: true)
                    depReport += sh(script: "[ -f build.gradle ] && git diff HEAD~1 HEAD -- build.gradle || echo ''", returnStdout: true)

                    // Collect environment variables
                    def envText = ""
                    env.each { key, value -> envText += "${key} = ${value}\n" }

                    // Build HTML dashboard
                    def htmlReport = """
                        <html>
                        <head>
                          <title>Branch Dashboard - ${BRANCH_NAME}</title>
                          <style>
                            body { font-family: Arial, sans-serif; margin: 20px; }
                            h2 { color: #2c3e50; }
                            pre { background: #f4f4f4; padding: 10px; border-radius: 8px; }
                            .section { margin-bottom: 20px; }
                          </style>
                        </head>
                        <body>
                          <h1>Branch: ${BRANCH_NAME} (${ENV_NAME})</h1>

                          <div class="section">
                            <h2>Commit Info</h2>
                            <pre>${commitInfo}</pre>
                          </div>

                          <div class="section">
                            <h2>Dependency Changes</h2>
                            <pre>${depReport ?: "No dependency changes detected"}</pre>
                          </div>

                          <div class="section">
                            <h2>Environment Variables</h2>
                            <pre>${envText}</pre>
                          </div>
                        </body>
                        </html>
                    """

                    writeFile file: "report.html", text: htmlReport
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', fingerprint: true
            publishHTML(target: [
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: "Branch Dashboard Report"
            ])
        }
    }
}
