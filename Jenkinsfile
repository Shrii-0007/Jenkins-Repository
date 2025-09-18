import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Branches in order
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def allSummaries = [:]  // Store summary of all branches

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // Checkout only the JSON file
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]]
                                ])

                                // Read and parse JSON
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new JsonSlurper().parseText(jsonText)

                                def branchSummary = []

                                // Loop through AppSettings array in JSON
                                json.AppSettings.each { app ->
                                    app.Settings.each { s ->
                                        def sqlConn = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"
                                        branchSummary << "SQL Connection: ${sqlConn}, Logging: ${logging}"
                                    }
                                }

                                // Print branch output like your requested style
                                echo "✅ ${branch} => \n\t• ${branchSummary.join("\n\t• ")}"

                                // Save for final summary
                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                                allSummaries[branch] = ["Config missing"]
                            }
                        }
                    }

                    // Final Summary for all branches
                    echo "\n📊 Final Summary (All Branches):"
                    allSummaries.each { br, vals ->
                        echo "📂 ${br} Results:\n\t• ${vals.join("\n\t• ")}"
                    }

                    echo "\n✅ All environment branches processed in order: Development → QA → UAT → Production"
                }
            }
        }
    }

    post {
        success { echo "✅ Pipeline completed successfully for all branches" }
        failure { echo "❌ Pipeline failed!" }
    }
}
