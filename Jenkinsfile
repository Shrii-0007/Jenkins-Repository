pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Branch list
                    def branches = ['Development','QA','UAT','UAT','Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        // Checkout branch silently
                        checkout([$class: 'GitSCM',
                                  branches: [[name: "refs/heads/${branch}"]],
                                  userRemoteConfigs: [[
                                      url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                      credentialsId: 'Github-Credential'
                                  ]],
                                  extensions: [
                                      [$class: 'CloneOption', shallow: true, depth: 1, noTags: true],
                                      [$class: 'CleanBeforeCheckout']
                                  ]
                        ])

                        def configFile = "appsettings.${branch}.json"

                        if (fileExists(configFile)) {
                            def json = readJSON file: configFile
                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def environmentName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                        } else {
                            echo "⚠ ${branch} → Config file not found, skipping."
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
