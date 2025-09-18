pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                // Checkout happens once only, so Blue Ocean shows single tab
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/main"]], // or your default branch
                    userRemoteConfigs: [[
                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                        credentialsId: 'Github-Credential'
                    ]]
                ])

                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def summary = []

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        try {
                            // Read JSON directly from workspace (no extra tab)
                            def jsonText = readFile("appsettings.${branch}.json")
                            def json = new groovy.json.JsonSlurper().parseText(jsonText)

                            def branchBlock = []
                            json.AppSettings.each { setting ->
                                setting.Settings.each { s ->
                                    def sqlConnection = s.Dev_MySql_Connection_String ?: "N/A"
                                    def logging = s.Logging ?: "N/A"
                                    branchBlock << "• SQL Connection: ${sqlConnection}, Logging: ${logging}"
                                }
                            }

                            // Branch-wise output in single block
                            echo "✅ ${branch} => " + branchBlock.join(" ")

                            // Add to summary
                            summary << "📂 ${branch} Results: " + branchBlock.join(" ")
                        }
                        catch (Exception e) {
                            def errorMsg = "⚠ ${branch} → Config file not found or invalid"
                            echo errorMsg
                            summary << errorMsg
                        }
                    }

                    // Final summary
                    echo "📊 Final Summary (All Branches):" + summary.join("")
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
