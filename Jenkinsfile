pipeline {
    agent any

    stages {
        stage('Approval Request') {
            steps {
                script {
                    emailext (
                        to: 'spkut1919@gmail.com',
                        subject: "🔔 Approval Required for Build #${env.BUILD_NUMBER}",
                        body: """
                            <h2>Build Approval Needed</h2>
                            <p>Hello,</p>
                            <p>Please review and approve the build:</p>
                            <ul>
                                <li>Job: ${env.JOB_NAME}</li>
                                <li>Build: #${env.BUILD_NUMBER}</li>
                                <li>URL: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></li>
                            </ul>
                            <p>Thanks,<br/>Jenkins</p>
                        """,
                        mimeType: 'text/html'
                    )
                }
            }
        }

        stage('Approval Decision') {
            steps {
                script {
                    timeout(time: 30, unit: 'MINUTES') {
                        input message: "Do you approve this build?", ok: "Approve"
                    }
                }
            }
        }
    }
}
