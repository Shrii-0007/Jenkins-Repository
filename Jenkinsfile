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

                        // Checkout only the specific branch silently
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "*/${branch}"]],
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [[$class: 'CloneOption', noTags: true, shallow: true, timeout: 10]],
                            userRemoteConfigs: [[
                                url: env.GIT_REPO,
                                credentialsId: env.GIT_CREDENTIALS
                            ]]
                        ])

                        def configFile = "appsettings.${branch}.json"
                        if (fileExists(configFile)) {
                            def config = readJSON file: configFile

                            def appName = config.AppSettings?.AppName ?: "N/A"
                            def version = config.AppSettings?.Version ?: "N/A"
                            def environment = config.AppSettings?.Environment ?: "N/A"
                            def extraVar = config.AppSettings?.ExtraVar ?: "N/A"

                            // ✅ Only this message will show on Blue Ocean
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
        success { echo "✅ All environment branches processed!" }
        failure { echo "❌ Pipeline failed!" }
    }
}
