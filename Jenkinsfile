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
                                            [path: "Dockerfile.${branch}"]
                                        ]]
                                    ]
                                ])

                                def branchSummary = []

                                // Read AppSettings JSON
                                def appsettingsFile = "appsettings.${branch}.json"
                                if (fileExists(appsettingsFile)) {
                                    def jsonText = readFile(appsettingsFile)
                                    def json = new JsonSlurper().parseText(jsonText)
                                    json.AppSettings.each { app ->
                                        app.Settings.each { s ->
                                            def sqlConn = s.Dev_MySql_Connection_String ?: "N/A"
                                            def logging = s.Logging ?: "N/A"
                                            branchSummary << [group: "AppSettings", variable: "SQL", value: sqlConn]
                                            branchSummary << [group: "AppSettings", variable: "Logging", value: logging]
                                        }
                                    }
                                } else {
                                    branchSummary << [group:"AppSettings", variable:"Missing", value:"File not found"]
                                }

                                // Read Dockerfile ENV variables
                                def dockerfileName = "Dockerfile.${branch}"
                                if (fileExists(dockerfileName)) {
                                    def dockerLines = readFile(dockerfileName).split("\n")
                                    dockerLines.each { line ->
                                        line = line.trim()
                                        if (line.startsWith("ENV") || line.startsWith("ARG")) {
                                            def parts = line.replaceFirst(/^(ENV|ARG)\s+/, "").split(/\s+/)
                                            parts.each { p ->
                                                if (p.contains("=")) {
                                                    def kv = p.split("=", 2)
                                                    branchSummary << [group: "Dockerfile", variable: kv[0], value: kv[1]]
                                                }
                                            }
                                        }
                                    }
                                } else {
                                    branchSummary << [group:"Dockerfile", variable:"Missing", value:"File not found"]
                                }

                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config or Dockerfile not found"
                                allSummaries[branch] = [[group:"Error", variable:"Config missing", value:"Config missing"]]
                            }
                        }
                    }

                    // Build HTML content
                    def htmlContent = """
                        <html>
                        <head>
                            <title>Environment Dashboard</title>
                            <style>
                                body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 20px; }
                                h1 { text-align: center; color: #333; margin-bottom: 30px; }
                                h2 { color: #2E8B57; border-bottom: 2px solid #ccc; padding-bottom: 5px; margin-top: 40px; }
                                table { border-collapse: collapse; width: 90%; margin: 20px auto; background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
                                th, td { border: 1px solid #ddd; padding: 12px 15px; text-align: left; }
                                th { background-color: #4CAF50; color: white; font-weight: bold; }
                                tr:nth-child(even) { background-color: #f9f9f9; }
                                tr:hover { background-color: #f1f1f1; }
                            </style>
                        </head>
                        <body>
                            <h1>🌍 Jenkins Environment Dashboard</h1>
                    """

                    branches.each { branch ->
                        htmlContent += "<h2>${branch} Environment</h2>"

                        // AppSettings table
                        def appSettings = allSummaries[branch].findAll { it.group == "AppSettings" }
                        if (appSettings) {
                            htmlContent += "<table><tr><th>Variable</th><th>Value</th></tr>"
                            appSettings.each { item ->
                                htmlContent += "<tr><td>${item.variable}</td><td>${item.value}</td></tr>"
                            }
                            htmlContent += "</table>"
                        }

                        // Dockerfile table
                        def dockerVars = allSummaries[branch].findAll { it.group == "Dockerfile" }
                        if (dockerVars) {
                            htmlContent += "<table><tr><th>Variable</th><th>Value</th></tr>"
                            dockerVars.each { item ->
                                htmlContent += "<tr><td>${item.variable}</td><td>${item.value}</td></tr>"
                            }
                            htmlContent += "</table>"
                        }
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
