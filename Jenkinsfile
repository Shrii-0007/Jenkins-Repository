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
                                // Checkout branch
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [
                                        [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [
                                            [path: "appsettings.${branch}.json"], 
                                            [path: "Dockerfile"]
                                        ]]
                                    ]
                                ])

                                // Read appsettings JSON
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new JsonSlurper().parseText(jsonText)
                                def branchSummary = []

                                json.AppSettings.each { app ->
                                    app.Settings.each { s ->
                                        def sqlConn = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"
                                        branchSummary << [type: "AppSettings", variable: "SQL", value: sqlConn]
                                        branchSummary << [type: "AppSettings", variable: "Logging", value: logging]
                                    }
                                }

                                // Read Dockerfile ENV variables
                                if (fileExists("Dockerfile")) {
                                    def dockerLines = readFile("Dockerfile").split("\n")
                                    dockerLines.each { line ->
                                        line = line.trim()
                                        if (line.startsWith("ENV") || line.startsWith("ARG")) {
                                            def parts = line.replaceFirst(/^(ENV|ARG)\s+/, "").split(/\s+/)
                                            parts.each { p ->
                                                if (p.contains("=")) {
                                                    def kv = p.split("=", 2)
                                                    branchSummary << [type: "Dockerfile", variable: kv[0], value: kv[1]]
                                                }
                                            }
                                        }
                                    }
                                }

                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                                allSummaries[branch] = [[type:"Error", variable: "Config missing", value: "Config missing"]]
                            }
                        }
                    }

                    // Build HTML content
                    def htmlContent = """
                        <html>
                        <head>
                            <title>Environment Dashboard</title>
                            <style>
                                body { font-family: Arial, sans-serif; background-color: #f7f7f7; }
                                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                                th { background-color: #4CAF50; color: white; }
                                tr:nth-child(even){ background-color: #f2f2f2; }
                                tr:hover { background-color: #ddd; }
                                h2 { color: #2E8B57; }
                            </style>
                        </head>
                        <body>
                            <h1>Jenkins Environment Dashboard</h1>
                    """

                    branches.each { branch ->
                        htmlContent += "<h2>${branch} Environment</h2>"
                        htmlContent += "<table><tr><th>Source</th><th>Variable</th><th>Value</th></tr>"
                        allSummaries[branch].each { item ->
                            htmlContent += "<tr><td>${item.type}</td><td>${item.variable}</td><td>${item.value}</td></tr>"
                        }
                        htmlContent += "</table>"
                    }

                    htmlContent += "</body></html>"

                    // Save HTML file in dashboard folder
                    writeFile file: 'dashboard/environment_dashboard.html', text: htmlContent

                    echo "✅ HTML dashboard created with AppSettings + Dockerfile ENV"
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
