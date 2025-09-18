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

                                // Print branch output immediately
                                echo "✅ ${branch} => \n\t• ${branchSummary.join("\n\t• ")}"

                                // Save for final summary
                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                                allSummaries[branch] = ["Config missing"]
                            }
                        }
                    }

                    // Print clean final summary like requested
                    echo "\n📊 Final Summary (All Branches):\n"

                    branches.each { branch ->
                        echo "📂 ${branch} Results:\n"
                        allSummaries[branch].each { val ->
                            echo "\t• ${val}"
                        }
                        echo "\n"  // Add empty line between branches
                    }

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
