pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Helper: quiet checkout (no logs)
                    def quietCheckout = { branch, path ->
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "origin/${branch}"]],
                            userRemoteConfigs: [[
                                url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                credentialsId: 'Github-Credential'
                            ]],
                            extensions: [
                                [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: path]]],
                                [$class: 'CloneOption', noTags: true, shallow: true, depth: 1]
                            ]
                        ])
                    }

                    // Branches in order
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // Silent checkout of only JSON file
                                quietCheckout(branch, "appsettings.${branch}.json")

                                // Read JSON quietly (no cat output)
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def version = json.AppSettings?.Version ?: "N/A"
                                def environmentName = json.AppSettings?.Environment ?: "N/A"
                                def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                                // Only clean output shown on dashboard
                                echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                            } catch (Exception e) {
                                // Silent skip if file or checkout fails
                                echo "⚠ ${branch} → Config file not found or branch missing"
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ All environment branches processed in order: Development → QA → UAT → Production"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
