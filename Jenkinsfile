pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
    }

    environment {
        GIT_REPO = "https://github.com/Shrii-0007/Jenkins-Repository.git"
        GIT_CREDENTIALS = "Github-Credential"
    }

    stages {

        stage('Process Environment Branches') {
            steps {
                script {
                    def envBranches = ['Development','QA','UAT','Production']

                    for (branch in envBranches) {
                        echo "🌿 Processing Branch: ${branch}"

                        // Checkout branch
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "*/${branch}"]],
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [],
                            userRemoteConfigs: [[
                                url: env.GIT_REPO,
                                credentialsId: env.GIT_CREDENTIALS
                            ]]
                        ])

                        def configFile = "appsettings.${branch}.json"

                        if (fileExists(configFile)) {
                            def config = readJSON file: configFile

                            // Read only non-sensitive info
                            def appName = config.AppSettings?.AppName ?: "N/A"
                            def version = config.AppSettings?.Version ?: "N/A"
                            def environment = config.AppSettings?.Environment ?: "N/A"
                            def extraVar = config.AppSettings?.ExtraVar ?: "N/A"

                            // Print concise info for dashboard
                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environment}, ExtraVar: ${extraVar}"

                        } else {
                            echo "⚠ ${branch} → Config file not found"
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
