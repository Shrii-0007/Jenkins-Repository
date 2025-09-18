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
                                // Quiet checkout of only JSON file
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]]
                                ])

                                // Read JSON quietly
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                // Iterate over AppSettings array
                                json.AppSettings.each { setting ->
                                    def appName = setting.AppName ?: "N/A"
                                    def version = setting.Settings[0]?.Version ?: "N/A"
                                    def extraVar = setting.Settings[0]?.ExtraVar ?: "N/A"
                                    def sqlConnection = setting.Settings[0]?.Dev_MySql_Connection_String ?: "N/A"
                                    def logging = setting.Settings[0]?.Logging ?: "N/A"

                                    echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, ExtraVar: ${extraVar}, SQL: ${sqlConnection}, Logging: ${logging}"
                                }

                            } catch (Exception e) {
                                // Silent skip if file or checkout fails
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
