pipeline {
    agent any

    environment {
        APP_NAME = "MyDotNetApp"
        SUMMARY = ""
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout Jenkinsfile') {
            steps {
                echo "🌿 Running pipeline from branch: ${env.BRANCH_NAME}"
                checkout scm
            }
        }

        stage('Process All Config Branches') {
            steps {
                script {
                    // Branches jithe appsettings files aahet
                    def envBranches = ["development", "qa", "uat", "prod", "main"]
                    SUMMARY = ""

                    envBranches.each { branch ->
                        if (sh(script: "git ls-remote --heads origin ${branch}", returnStatus: true) == 0) {
                            echo "✅ Found branch: ${branch}"

                            // Fetch branch and copy appsettings
                            sh "git fetch origin ${branch}:${branch}"
                            sh "git checkout ${branch} -- appsettings.${branch.capitalize()}.json || echo 'No appsettings found'"

                            // Default fallback
                            def appEnv = branch.capitalize()
                            def appVersion = "N/A"

                            // Read version from JSON if exists
                            if (fileExists("appsettings.${appEnv}.json")) {
                                def json = readJSON file: "appsettings.${appEnv}.json"
                                appVersion = json?.Version ?: "N/A"
                            }

                            SUMMARY += "Branch: ${branch}, Env: ${appEnv}, Version: ${appVersion}\n"

                            // Optional: build only main/development
                            if (branch == "main" || branch == "development") {
                                sh "dotnet restore"
                                sh "dotnet build --configuration Release /p:Version=${appVersion}"
                            }
                        } else {
                            echo "⚠️ Branch not found: ${branch}"
                        }
                    }

                    echo "\n📊 Summary of all branches:\n${SUMMARY}"
                }
            }
        }
    }

    post {
        always {
            echo "📝 Final Branch Summary:\n${SUMMARY}"
        }
    }
}
