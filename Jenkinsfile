pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Approval Request') {
            steps {
                emailext(
                    subject: "🔔 Approval Needed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        <html>
                          <body style="font-family: Arial, sans-serif; color: #333;">
                            <h2 style="color:#2E86C1;">Build Approval Required</h2>
                            <p>Hello Team,</p>
                            <p>
                              The build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> requires your approval before it can continue.
                            </p>
                            <p>
                              <a href="${env.BUILD_URL}" style="background:#2E86C1; color:#fff; padding:10px 15px; text-decoration:none; border-radius:5px;">
                                🔗 Review Build
                              </a>
                            </p>
                            <p>Thanks,<br/>Jenkins CI/CD</p>
                          </body>
                        </html>
                    """,
                    to: "spkute2020@gmail.com",
                    mimeType: 'text/html'
                )
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
        success { echo "✅ All environment branches processed successfully after approval." }
        failure { echo "❌ Pipeline failed or was rejected." }
    }
}
