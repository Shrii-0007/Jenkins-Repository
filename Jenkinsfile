pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    def branches = ['Development','QA','UAT','Production']

                    branches.each { branch ->
                        // Quietly fetch & checkout branch
                        sh """
                        git fetch origin ${branch}:${branch} --quiet
                        git checkout ${branch} --quiet
                        """

                        // Read JSON silently
                        def configFile = "appsettings.${branch}.json"
                        if (new File(configFile).exists()) {
                            def jsonText = new File(configFile).text
                            def json = new groovy.json.JsonSlurper().parseText(jsonText)

                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def envName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            echo "🌿 Processing Branch: ${branch}"
                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${envName}, ExtraVar: ${extraVar}"
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
