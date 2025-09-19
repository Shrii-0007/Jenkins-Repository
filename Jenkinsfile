import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def allSummaries = [:]

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

                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file missing"
                                allSummaries[branch] = ["Config missing"]
                            }
                        }
                    }

                    // **Generate HTML**
                    def html = "<html><head><title>Branch Dashboard</title></head><body>"
                    html += "<h1>📊 Branch Dashboard</h1>"

                    branches.each { branch ->
                        html += "<h2>${branch} Results:</h2><ul>"
                        allSummaries[branch].each { val ->
                            html += "<li>${val}</li>"
                        }
                        html += "</ul>"
                    }

                    html += "</body></html>"

                    writeFile file: 'dashboard.html', text: html

                    echo "✅ Dashboard generated successfully: dashboard.html"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully for all branches"

            // Publish HTML
            publishHTML([
                reportDir: '.',          // dashboard.html is in workspace root
                reportFiles: 'dashboard.html',
                reportName: 'Branch Dashboard',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
        }
        failure { echo "❌ Pipeline failed!" }
    }
}
