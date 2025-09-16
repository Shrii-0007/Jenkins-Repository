pipeline {
    agent any

    stages {
        stage('Basic Mail Test') {
            steps {
                emailext(
                    to: 'spkute1919@gmail.com',
                    subject: "✅ Pipeline Plain Mail Test - Job ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """Hello Team,

This is a plain text test mail from Jenkins Pipeline.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}

Regards,
Jenkins
"""
                )
            }
        }
    }

    post {
        success {
            echo "✅ Mail stage executed successfully."
        }
        failure {
            echo "❌ Mail stage failed."
        }
    }
}
