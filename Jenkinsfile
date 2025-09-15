import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    def branches = ['Development','QA','UAT','Production']

                    branches.each { branch ->

                        def configFile = "${WORKSPACE}/appsettings.${branch}.json"

                        if (new File(configFile).exists()) {
                            // Read JSON with Groovy JsonSlurper
                            def jsonText = new File(configFile).text
                            def json = new JsonSlurper().parseText(jsonText)

                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def environmentName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            echo "🌿 Processing Branch: ${branch}"
                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                        }
                        // If the file does not exist, do nothing — no ⚠ message
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
