pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Generate Dashboard') {
            steps {
                // Make sure Python virtual env is activated if used
                sh '''
                # Optional: activate venv if you use one
                # source ~/myenv/bin/activate

                python3 generate_dashboards.py
                '''
            }
        }

        stage('Publish Dashboard') {
            steps {
                publishHTML([
                    reportDir: '.',               // current workspace
                    reportFiles: 'dashboard.html',
                    reportName: 'Branch Dashboard',
                    keepAll: true,
                    alwaysLinkToLastBuild: true
                ])
            }
        }
    }

    post {
        success { echo "✅ Pipeline completed successfully for all branches" }
        failure { echo "❌ Pipeline failed!" }
    }
}
