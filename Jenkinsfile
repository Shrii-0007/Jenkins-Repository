pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // Checkout फक्त JSON
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [[
                                        $class: 'SparseCheckoutPaths',
                                        sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]
                                    ]]
                                ])

                                // File वाचताना unwanted log suppress
                                def jsonText = sh(
                                    script: "cat appsettings.${branch}.json",
                                    returnStdout: true
                                ).trim()

                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def versions = json.AppSettings?.Version ?: []
                                def envs = json.AppSettings?.Environment ?: []
                                def extras = json.AppSettings?.ExtraVar ?: []

                                // फक्त हीच लाइन dashboard वर दिसेल
                                echo "✅ ${branch} → AppName: [${appName}], Version: ${versions}, Env: ${envs}, ExtraVar: ${extras}"

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
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
