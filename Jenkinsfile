pipeline {
    agent any
    options {
        timestamps()
    }
    environment {
        DOTNET_ROOT = "/usr/share/dotnet" // optional
    }
    stages {
        stage('Checkout SCM') {
            steps {
                echo "🌿 Checking out main branch"
                checkout scm
            }
        }

        stage('Process Environments & Generate Dashboard') {
            steps {
                script {
                    // Define all environments
                    def envBranches = ['Development', 'QA', 'UAT', 'Production']
                    def results = [:]  // store HTML for each env

                    envBranches.each { envName ->
                        dir("tmp_${envName}") {
                            checkout([$class: 'GitSCM',
                                branches: [[name: "origin/${envName}"]],
                                doGenerateSubmoduleConfigurations: false,
                                extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "."]],
                                userRemoteConfigs: [[
                                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                    credentialsId: 'Github-Credential'
                                ]]
                            ])

                            // Read branch-specific config
                            def content = readFile "appsettings.${envName}.json"
                            // Example: extract SQL info (you can customize)
                            def sqlInfo = content.readLines().findAll { it.contains("Server") || it.contains("Database") }.join("<br>")
                            results[envName] = sqlInfo
                        }
                    }

                    // Generate HTML
                    def html = """
                    <html>
                    <head><title>Branch Dashboard</title></head>
                    <body>
                        <h1>📊 Branch Dashboard</h1>
                    """
                    envBranches.each { envName ->
                        html += "<h2>${envName}</h2><p>${results[envName]}</p>"
                    }
                    html += """
                    </body>
                    </html>
                    """

                    writeFile file: 'dashboard.html', text: html
                }
            }
        }
    }
    post {
        success {
            publishHTML(target: [
                reportDir: '.', 
                reportFiles: 'dashboard.html', 
                reportName: 'Branch Dashboard', 
                keepAll: true, 
                alwaysLinkToLastBuild: true
            ])
        }
    }
}
