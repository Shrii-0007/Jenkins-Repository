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

                    // Create folder for dashboard
                    sh 'mkdir -p dashboard'

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
                                        branchSummary << [sql: sqlConn, logging: logging]
                                    }
                                }

                                // Store for final HTML dashboard
                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                                allSummaries[branch] = [["sql": "Config missing", "logging": "Config missing"]]
                            }
                        }
                    }

                    // Build HTML content
                    def htmlContent = """
                        <html>
                        <head>
                            <title>Environment Dashboard</title>
                            <style>
                                body { font-family: Arial, sans-serif; }
                                table { border-collapse: collapse; width: 80%; margin-bottom: 20px; }
                                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                                th { background-color: #f2f2f2; }
                                h2 { color: #2e6c80; }
                            </style>
                        </head>
                        <body>
                            <h1>Jenkins Environment Dashboard</h1>
                    """

                    branches.each { branch ->
                        htmlContent += "<h2>${branch} Environment</h2>"
                        htmlContent += "<table><tr><th>SQL Connection</th><th>Logging</th></tr>"
                        allSummaries[branch].each { item ->
                            htmlContent += "<tr><td>${item.sql}</td><td>${item.logging}</td></tr>"
                        }
                        htmlContent += "</table>"
                    }

                    htmlContent += "</body></html>"

                    // Save HTML file in dashboard folder
                    writeFile file: 'dashboard/environment_dashboard.html', text: htmlContent

                    echo "✅ HTML dashboard created"
                }
            }
        }

        stage('Publish Dashboard') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'dashboard',
                    reportFiles: 'environment_dashboard.html',
                    reportName: 'Environment Dashboard'
                ])
            }
        }
    }

    post {
        success { echo "✅ Pipeline completed successfully for all branches" }
        failure { echo "❌ Pipeline failed!" }
    }
}
