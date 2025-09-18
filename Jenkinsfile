pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Branches in order
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def summary = []

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
                                    extensions: [[$class: 'SparseCheckoutPaths',
                                                  sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]]
                                ])

                                // Read and parse JSON file
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                // Iterate over settings for this branch
                                def branchResults = []
                                json.AppSettings.each { setting ->
                                    setting.Settings.each { s ->
                                        def sqlConnection = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"

                                        def result = "✅ ${branch} → SQL Connection: ${sqlConnection}, Logging: ${logging}"
                                        echo result            // Branch-wise output
                                        branchResults << result // Collect for summary
                                    }
                                }

                                // Add to final summary
                                summary += branchResults

                            } catch (Exception e) {
                                def errorMsg = "⚠ ${branch} → Config file not found or branch missing"
                                echo errorMsg
                                summary << errorMsg
                            }
                        }
                    }

                    // Print combined clean output at once (final summary)
                    echo "\n📊 Final Summary:\n" + summary.join("\n")
                }
            }
        }
    }

    post {
        success {
            echo "✅ All environment branches processed in order: Development → QA → UAT → Production"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
