pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Branches in order
                    def branches = ['Development', 'QA', 'UAT', 'Production']

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

                                // Read JSON file
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                // Iterate over AppSettings array and all Settings objects
                                json.AppSettings.each { setting ->
                                    setting.Settings.each { s ->
                                        def sqlConnection = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"

                                        echo "✅ ${branch} → SQL Connection: ${sqlConnection}, Logging: ${logging}"
                                    }
                                }

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
        success { echo "✅ All environment branches processed in order: Development → QA → UAT → Production" }
        failure { echo "❌ Pipeline failed!" }
    }
}
