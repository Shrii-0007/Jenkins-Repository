pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Desired branch order
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        // Use a temporary folder for checkout to hide SCM logs
                        dir("tmp_${branch}") {
                            // Checkout only JSON file quietly
                            checkout([
                                $class: 'GitSCM',
                                branches: [[name: "origin/${branch}"]],
                                userRemoteConfigs: [[
                                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                    credentialsId: 'Github-Credential'
                                ]],
                                extensions: [[$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]]
                            ])

                            def configFile = "appsettings.${branch}.json"
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
    }

    post {
        success { echo "✅ All environment branches processed in order: Development → QA → UAT → Production" }
        failure { echo "❌ Pipeline failed!" }
    }
}
