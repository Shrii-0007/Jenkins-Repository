pipeline {
    agent any

    stages {
        stage('Send Email') {
            steps {
                emailext(
                    to: 'spkute1919@gmail.com',
                    from: 'yourgmail@gmail.com',  // must match the Gmail you configured in Jenkins
                    subject: "✅ Jenkins Pipeline Mail Test - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        <html>
                          <body>
                            <h2 style="color:green;">Jenkins Mail Test</h2>
                            <p>Hello Team,</p>
                            <p>This is a <b>test email</b> sent from the Jenkins Pipeline.</p>
                            <p>
                              <b>Job:</b> ${env.JOB_NAME}<br/>
                              <b>Build:</b> #${env.BUILD_NUMBER}<br/>
                              <b>URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a>
                            </p>
                            <p>Regards,<br/>Jenkins</p>
                          </body>
                        </html>
                    """,
                    mimeType: 'text/html'
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
