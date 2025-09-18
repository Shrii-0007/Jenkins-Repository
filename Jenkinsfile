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
                                // Run checkout in shell to avoid Blue Ocean tabs
                                sh """
                                    git init
                                    git remote add origin https://github.com/Shrii-0007/Jenkins-Repository.git || true
                                    git fetch --depth=1 origin ${branch}
                                    git checkout FETCH_HEAD
                                """

                                // Read JSON with shell & Groovy (no 'readFile' tab)
                                def jsonText = sh(
                                    script: "cat appsettings.${branch}.json",
                                    returnStdout: true
                                ).trim()

                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                // Collect results branch-wise
                                def branchBlock = []
                                json.AppSettings.each { setting ->
                                    setting.Settings.each { s ->
                                        def sqlConnection = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"
                                        branchBlock << "   • SQL Connection: ${sqlConnection}, Logging: ${logging}"
                                    }
                                }

                                // Print grouped output
                                echo "✅ ${branch} =>\n" + branchBlock.join("\n")

                                // Add to summary
                                summary << "📂 ${branch} Results:\n" + branchBlock.join("\n")

                            } catch (Exception e) {
                                def errorMsg = "⚠ ${branch} → Config file not found or branch missing"
                                echo errorMsg
                                summary << errorMsg
                            }
                        }
                    }

                    // Print final summary
                    echo "\n📊 Final Summary (All Branches):\n" + summary.join("\n\n")
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
