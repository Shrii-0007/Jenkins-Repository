import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    // Define branches
                    def branches = ['Development','QA','UAT','Production']

                    branches.each { branch ->

                        echo "🌿 Processing Branch: ${branch}"

                        // Use pure Groovy to read the JSON file
                        def configFile = "appsettings.${branch}.json"
                        def appName = "N/A"
                        def version = "N/A"
                        def environmentName = "N/A"
                        def extraVar = "N/A"

                        // Use try-catch to avoid pipeline step logging
                        try {
                            // Read file content using Groovy File class, not Jenkins step
                            def jsonText = new File("${WORKSPACE}/${configFile}").text
                            def json = new JsonSlurper().parseText(jsonText)

                            appName = json.AppSettings?.AppName ?: "N/A"
                            version = json.AppSettings?.Version ?: "N/A"
                            environmentName = json.AppSettings?.Environment ?: "N/A"
                            extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                        } catch (Exception e) {
                            // File not found or parse error
                            echo "⚠ ${branch} → Config file not found or invalid"
                        }

                        // Only this message will appear on Blue Ocean
                        echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
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
