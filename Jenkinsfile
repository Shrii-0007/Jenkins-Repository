pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Environment Branches') {
            steps {
                script {
                    // Correct branch list (unique)
                    def branches = ['Development','QA','UAT','Production']

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

                        // Read JSON file
                        def configFile = "appsettings.${branch}.json"

                        if (fileExists(configFile)) {
                            def json = readJSON file: configFile
                            def appName = json.AppSettings?.AppName ?: "N/A"
                            def version = json.AppSettings?.Version ?: "N/A"
                            def envName = json.AppSettings?.Environment ?: "N/A"
                            def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                            // Echo only your desired content
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
