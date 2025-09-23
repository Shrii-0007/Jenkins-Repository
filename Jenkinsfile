import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def envColors = [
                        Development: "#e3f2fd",   // Light Blue
                        QA: "#fff3e0",            // Light Orange
                        UAT: "#f3e5f5",           // Light Purple
                        Production: "#e8f5e9"     // Light Green
                    ]
                    def allSummaries = [:]

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
                                    extensions: [
                                        [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [
                                            [path: "appsettings.${branch}.json"], 
                                            [path: "Dockerfile.${branch}"],
                                            [path: "env_dashboard_template.html"]
                                        ]]
                                    ]
                                ])

                                def branchSummary = []

                                // AppSettings JSON
                                def appsettingsFile = "appsettings.${branch}.json"
                                if (fileExists(appsettingsFile)) {
                                    def jsonText = readFile(appsettingsFile)
                                    def json = new JsonSlurper().parseText(jsonText)
                                    json.AppSettings.each { app ->
                                        app.Settings.each { s ->
                                            branchSummary << [variable: "SQL", value: (s.Dev_MySql_Connection_String ?: "N/A")]
                                            branchSummary << [variable: "Logging", value: (s.Logging ?: "N/A")]
                                        }
                                    }
                                }

                                // Dockerfile.<branch>
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
                                                    branchSummary << [variable: kv[0], value: kv[1]]
                                                }
                                            }
                                        }
                                    }
                                }

                                allSummaries[branch] = branchSummary

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config or Dockerfile not found"
                                allSummaries[branch] = [[variable:"Missing", value:"File not found"]]
                            }
                        }
                    }

                    // Load Template
                    def templateFile = "tmp_Development/env_dashboard_template.html"
                    def templateContent = readFile(templateFile)

                    // Build Environment Sections
                    def envSections = ""
                    branches.each { branch ->
                        def color = envColors[branch] ?: "#ffffff"
                        def tableRows = ""
                        allSummaries[branch].each { item ->
                            tableRows += "<tr><td class='variable'>${item.variable}</td><td class='value'>${item.value}</td></tr>"
                        }
                        envSections += """
                            <div class='env-section' style='background-color:${color};'>
                                <h2>${branch} Environment</h2>
                                <table>
                                    <tr><th>Variable</th><th>Value</th></tr>
                                    ${tableRows}
                                </table>
                            </div>
                        """
                    }

                    // Replace placeholder in template
                    def finalHtml = templateContent.replace("{{ENV_SECTIONS}}", envSections)

                    // Save HTML
                    writeFile file: 'dashboard/environment_dashboard.html', text: finalHtml
                    echo "✅ Dashboard created from template"
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
        success { echo "✅ Pipeline completed successfully" }
        failure { echo "❌ Pipeline failed!" }
    }
}
