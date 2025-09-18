pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Branches in order
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        try {
                            dir("tmp_${branch}") {
                                // Silent checkout
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [
                                        [$class: 'SparseCheckoutPaths',
                                         sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]],
                                        [$class: 'CloneOption',
                                         shallow: true, depth: 1, noTags: true, reference: '', timeout: 10, quiet: true]
                                    ]
                                ])

                                // Read JSON (Jenkins won't show file read step now)
                                def json = new groovy.json.JsonSlurper().parseText(
                                    readFile("appsettings.${branch}.json")
                                )

                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def version = json.AppSettings?.Version ?: "N/A"
                                def environmentName = json.AppSettings?.Environment ?: "N/A"
                                def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                                // 👉 Only this will appear in Jenkins Dashboard
                                echo "🌿 Branch: ${branch}"
                                echo "   AppName     : ${appName}"
                                echo "   Version     : ${version}"
                                echo "   Environment : ${environmentName}"
                                echo "   Variables   : ${extraVar}"
                                echo "-------------------------------------------"
                            }
                        } catch (Exception e) {
                            echo "⚠ ${branch} → Config file not found or branch missing"
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
