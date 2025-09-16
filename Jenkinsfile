pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Approval Request') {
            steps {
                script {
                    emailext(
                        subject: "🔔 Approval Needed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """
                            <html>
                              <body>
                                <h2>Build Approval Required</h2>
                                <p>Hello Team,</p>
                                <p>The build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> requires approval.</p>
                                <p>
                                  <a href="${env.BUILD_URL}">Click here to review and approve</a>
                                </p>
                              </body>
                            </html>
                        """,
                        to: "spkute2020@gmail.com",
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

        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [[
                                        $class: 'SparseCheckoutPaths',
                                        sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]
                                    ]]
                                ])

                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def version = json.AppSettings?.Version ?: "N/A"
                                def environmentName = json.AppSettings?.Environment ?: "N/A"
                                def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                                echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            emailext(
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <html>
                      <body>
                        <h2>Build Completed Successfully</h2>
                        <p>All branches processed after approval ✅</p>
                        <p><a href="${env.BUILD_URL}">Click here for details</a></p>
                      </body>
                    </html>
                """,
                to: "spkute2020@gmail.com",
                mimeType: 'text/html'
            )
        }
        failure {
            emailext(
                subject: "❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <html>
                      <body>
                        <h2>Build Failed</h2>
                        <p>Please check logs for more details ⚠</p>
                        <p><a href="${env.BUILD_URL}">Click here for logs</a></p>
                      </body>
                    </html>
                """,
                to: "spkute2020@gmail.com",
                mimeType: 'text/html'
            )
        }
    }
}
