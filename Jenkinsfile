pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    // List of environment branches
                    def branches = ['Development','QA','UAT','Production']

                    branches.each { branch ->
                        def configFile = "appsettings.${branch}.json"

                        // Check if file exists
                        if (fileExists(configFile)) {
                            // Read JSON using readJSON step (sandbox safe)
                            def json = readJSON file: configFile

                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def environmentName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            echo "🌿 Processing Branch: ${branch}"
                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                        }
                        // If file doesn't exist, skip silently
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
