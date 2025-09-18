pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    // Define branches
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // Clean checkout with no Git noise
                                sh """
                                  rm -rf .git > /dev/null 2>&1 || true
                                  git init -q .
                                  git remote add origin https://github.com/Shrii-0007/Jenkins-Repository.git
                                  git fetch --depth=1 origin ${branch} > /dev/null 2>&1
                                  git checkout FETCH_HEAD -- appsettings.${branch}.json > /dev/null 2>&1
                                """

                                // Read JSON
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                // Extract values
                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def versions = json.AppSettings?.Version ?: []
                                def envs = json.AppSettings?.Environment ?: []
                                def extras = json.AppSettings?.ExtraVar ?: []

                                // Final clean output to dashboard
                                echo "✅ ${branch} → AppName: [${appName}], Versions: ${versions}, Envs: ${envs}, ExtraVars: ${extras}"

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
        success {
            echo "✅ All environment branches processed: Development → QA → UAT → Production"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
