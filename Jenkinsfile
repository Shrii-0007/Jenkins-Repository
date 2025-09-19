pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
    }
    environment {
        DOTNET_ROOT = "/usr/share/dotnet" // adjust if needed
        DASHBOARD_FILE = "dashboard.html"
    }
    stages {
        stage('Checkout') {
            steps {
                echo "🌿 Checking out main branch..."
                checkout([$class: 'GitSCM',
                    branches: [[name: "refs/heads/main"]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                        credentialsId: 'Github-Credential'
                    ]]
                ])
            }
        }

        stage('Generate Dashboard') {
            steps {
                script {
                    // Define branch/environment info
                    def envBranches = [
                        [name: 'Development', file: 'appsettings.Development.json'],
                        [name: 'QA',          file: 'appsettings.QA.json'],
                        [name: 'UAT',         file: 'appsettings.UAT.json'],
                        [name: 'Production',  file: 'appsettings.Production.json']
                    ]

                    // Start HTML content
                    def htmlContent = """
                    <html>
                    <head>
                        <title>Environment Dashboard</title>
                        <style>
                            body { font-family: Arial, sans-serif; padding: 20px; }
                            h2 { color: #2E86C1; }
                            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                            th, td { border: 1px solid #ddd; padding: 8px; }
                            th { background-color: #f2f2f2; }
                        </style>
                    </head>
                    <body>
                    <h1>Environment Dashboard - Main Branch</h1>
                    """

                    // Loop through each environment and read SQL info
                    envBranches.each { envInfo ->
                        def fileContent = readFile(envInfo.file)
                        htmlContent += "<h2>${envInfo.name}</h2><pre>${fileContent}</pre>"
                    }

                    htmlContent += "</body></html>"

                    // Write HTML file
                    writeFile file: DASHBOARD_FILE, text: htmlContent
                }
            }
        }

        stage('Publish Dashboard') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: ".",
                    reportFiles: "dashboard.html",
                    reportName: "Branch Dashboard"
                ])
            }
        }
    }

    post {
        success {
            echo "✅ Dashboard generated and published successfully!"
        }
        failure {
            echo "❌ Pipeline failed."
        }
    }
}
