pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Define environment branches
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        // Compose JSON file name per branch
                        def configFile = "appsettings.${branch}.json"

                        echo "🌿 Processing Branch: ${branch}"

                        // Sandbox-safe: Check file existence and read content
                        if (fileExists(configFile)) {
                            def jsonText = readFile(configFile)
                            def json = new groovy.json.JsonSlurper().parseText(jsonText)

                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def environmentName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                        } else {
                            echo "⚠ ${branch} → Config file not found"
                        }
                    }
                }
            }
        }
    }

    post {
        success { echo "✅ All environment branches processed!" }
        failure { echo "❌ Pipeline failed!" }
    }
}
