pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    // Define your environment branches
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        // Fetch and checkout branch silently
                        sh """
                            git fetch origin ${branch}:${branch} --quiet || true
                            git checkout ${branch} --quiet || true
                        """

                        // Check for env file (json/properties)
                        if (fileExists("appsettings.${branch}.json")) {
                            def jsonText = readFile("appsettings.${branch}.json")
                            def json = new groovy.json.JsonSlurper().parseText(jsonText)

                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def environmentName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                        } else if (fileExists("src/main/resources/application-${branch.toLowerCase()}.properties")) {
                            // For Java Spring Boot projects
                            def props = readProperties(file: "src/main/resources/application-${branch.toLowerCase()}.properties")
                            echo "✅ ${branch} → AppName: ${props['app.name']}, Version: ${props['app.version']}, Env: ${props['app.environment']}, ExtraVar: ${props['app.extraVar']}"
                        } else {
                            echo "⚠ ${branch} → No config file found!"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ All environment branches processed!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
