pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Approval Before Processing') {
            steps {
                script {
                    emailext (
                        to: 'spkute2020@gmail.com',
                        subject: "🔔 Approval Required - Jenkins Pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """<p>Hello,</p>
                                 <p>Pipeline <b>${env.JOB_NAME}</b> build #${env.BUILD_NUMBER} is waiting for approval.</p>
                                 <p>Please login to Jenkins and approve/reject the build.</p>
                                 <p><a href="${env.BUILD_URL}input">Click here to approve</a></p>"""
                    )

                    // Wait for manual approval inside Jenkins
                    timeout(time: 1, unit: 'HOURS') {
                        input message: "Do you approve to proceed with processing all environment branches?", ok: "Approve"
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
                                    extensions: [[$class: 'SparseCheckoutPaths',
                                        sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]
                                    ]
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
            emailext (
                to: 'spkute2020@gmail.com',
                subject: "✅ Jenkins Pipeline SUCCESS - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """<p>Pipeline completed successfully.</p>
                         <p>Check Jenkins: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>"""
            )
        }
        failure {
            emailext (
                to: 'spkute2020@gmail.com',
                subject: "❌ Jenkins Pipeline FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """<p>Pipeline failed.</p>
                         <p>Check logs: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>"""
            )
        }
    }
}
