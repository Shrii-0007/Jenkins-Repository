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
                                // Checkout only the JSON file (hidden from Blue Ocean as step noise)
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

                                // Iterate over settings
                                json.AppSettings.each { setting ->
                                    setting.Settings.each { s ->
                                        def sqlConnection = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"

                                        // Collect result instead of echoing directly
                                        summary << "✅ ${branch} → SQL Connection: ${sqlConnection}, Logging: ${logging}"
                                    }
                                }

                            } catch (Exception e) {
                                summary << "⚠ ${branch} → Config file not found or branch missing"
                            }
                        }
                    }

                    // Print combined clean output at once
                    echo "📊 Final Summary:\n" + summary.join("\n")
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
