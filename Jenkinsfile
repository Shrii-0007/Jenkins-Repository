import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def allSummaries = [:]  // Store summary of all branches

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
                                    extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]]
                                ])

                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new JsonSlurper().parseText(jsonText)

                                def branchSummary = []

                                json.AppSettings.each { app ->
                                    app.Settings.each { s ->
                                        def sqlConn = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"
                                        branchSummary << "SQL Connection: ${sqlConn}, Logging: ${logging}"
                                    }
                                }

                                // Store for final summary
                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                allSummaries[branch] = ["Config missing"]
                            }
                        }
                    }

                    // Build a single string for the final summary
                    def finalSummary = "\n📊 Final Summary (All Branches):\n"
                    branches.each { branch ->
                        finalSummary += "\n📂 ${branch} Results:\n"
                        allSummaries[branch].each { val ->
                            finalSummary += "\t• ${val}\n"
                        }
                    }

                    // Echo **once** for clean log output
                    echo finalSummary

                    echo "✅ All environment branches processed in order: Development → QA → UAT → Production"
                }
            }
        }
    }

    post {
        success { echo "✅ Pipeline completed successfully for all branches" }
        failure { echo "❌ Pipeline failed!" }
    }
}
