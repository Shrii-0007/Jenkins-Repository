pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
    }

    environment {
        GIT_REPO = "https://github.com/Shrii-0007/Jenkins-Repository.git"
        GIT_CREDENTIALS = "Github-Credential"
    }

    stages {

        stage('Process Environment Branches') {
            steps {
                script {
                    def envBranches = ['Development','QA','UAT','Production']
                    def dashboardData = []

                    for (branch in envBranches) {
                        echo "🌿 Processing Branch: ${branch}"

                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "*/${branch}"]],
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [],
                            userRemoteConfigs: [[
                                url: env.GIT_REPO,
                                credentialsId: env.GIT_CREDENTIALS
                            ]]
                        ])

                        def configFile = "appsettings.${branch}.json"

                        if (fileExists(configFile)) {
                            def config = readJSON file: configFile

                            // Read AppSettings safely
                            def appName = config.AppSettings?.AppName ?: "N/A"
                            def version = config.AppSettings?.Version ?: "N/A"
                            def environment = config.AppSettings?.Environment ?: "N/A"
                            def extraVar = config.AppSettings?.ExtraVar ?: "N/A"

                            echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environment}, ExtraVar: ${extraVar}"

                            // Do NOT include DB_URL or other secrets
                            dashboardData << [
                                branch: branch,
                                appName: appName,
                                version: version,
                                environment: environment,
                                extraVar: extraVar
                            ]
                        } else {
                            echo "⚠ ${branch} → Config file not found, skipping..."
                        }
                    }

                    // Write dashboard summary JSON without credentials
                    writeJSON file: 'dashboard_summary.json', json: dashboardData, pretty: 4

                    // Archive artifact for Blue Ocean
                    archiveArtifacts artifacts: 'dashboard_summary.json', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo "✅ Dashboard artifact created for all environment branches (no credentials included)!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
