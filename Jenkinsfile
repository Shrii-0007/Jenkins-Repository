pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Branchwise Dashboard Data') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']

                    branches.each { branch ->
                        dir("tmp_${branch}") {
                            try {
                                // Checkout only required config file
                                sh """
                                  rm -rf .git > /dev/null 2>&1 || true
                                  git init -q .
                                  git remote add origin https://github.com/Shrii-0007/Jenkins-Repository.git
                                  git fetch --depth=1 origin ${branch} > /dev/null 2>&1
                                  git checkout FETCH_HEAD -- appsettings.${branch}.json > /dev/null 2>&1
                                """

                                // Read JSON
                                def json = new groovy.json.JsonSlurper().parseText(
                                    readFile("appsettings.${branch}.json")
                                )

                                // Extract only required fields
                                def versions = json.AppSettings?.Version ?: []
                                def envs = json.AppSettings?.Environment ?: []
                                def extras = json.AppSettings?.ExtraVar ?: []

                                // 🎯 Final clean output (only what you want)
                                echo "📌 Branch: ${branch}"
                                echo "   Versions   : ${versions}"
                                echo "   Environments: ${envs}"
                                echo "   Variables  : ${extras}"
                                echo "----------------------------------------"

                            } catch (Exception e) {
                                echo "⚠ ${branch} → config not found"
                            }
                        }
                    }
                }
            }
        }
    }
}
