pipeline {
    agent any
    options { timestamps() }

    environment {
        GIT_REPO = "https://github.com/Shrii-0007/Jenkins-Repository.git"
        GIT_CREDENTIALS = "Github-Credential"
    }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    def branches = ['Development','QA','UAT','Production']

                    for (branch in branches) {
                        echo "🌿 Processing Branch: ${branch}"

                        // Use shell to fetch the appsettings JSON from Git without creating SCM steps in Blue Ocean
                        sh """
                            git fetch origin ${branch}:${branch} --quiet
                            git checkout ${branch} --quiet
                        """

                        // Read JSON manually using Groovy
                        def configFile = "appsettings.${branch}.json"
                        def appName = "N/A"
                        def version = "N/A"
                        def environmentName = "N/A"
                        def extraVar = "N/A"

                        if (fileExists(configFile)) {
                            def jsonText = readFile(configFile)
                            def json = new groovy.json.JsonSlurper().parseText(jsonText)

                            appName = json.AppSettings?.AppName ?: "N/A"
                            version = json.AppSettings?.Version ?: "N/A"
                            environmentName = json.AppSettings?.Environment ?: "N/A"
                            extraVar = json.AppSettings?.ExtraVar ?: "N/A"
                        }

                        // ✅ Only this message will show on Blue Ocean
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
