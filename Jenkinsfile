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
                                // SCM checkout logs hide करण्यासाठी redirect
                                sh(script: """
                                    git init -q
                                    git remote add origin https://github.com/Shrii-0007/Jenkins-Repository.git
                                    git fetch --depth 1 origin ${branch} -q
                                    git checkout FETCH_HEAD -q
                                """, returnStdout: true)

                                // फक्त appsettings file read
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def version = json.AppSettings?.Version ?: "N/A"
                                def environmentName = json.AppSettings?.Environment ?: "N/A"
                                def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                                // Dashboard वर फक्त हीच लाइन दिसेल
                                echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
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
        success { echo "✅ All environment branches processed successfully!" }
        failure { echo "❌ Pipeline failed!" }
    }
}
