pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Running build...'
            }
        }
    }

    post {
        always {
            emailext(
                subject: "Build ${currentBuild.currentResult}: ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: """
                    <p>Job: ${env.JOB_NAME}</p>
                    <p>Build Number: ${env.BUILD_NUMBER}</p>
                    <p>Status: ${currentBuild.currentResult}</p>
                """,
                to: 'recipient@example.com',
                mimeType: 'text/html'
            )
        }
    }
}
