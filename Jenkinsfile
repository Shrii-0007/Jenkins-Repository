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

                        // Checkout branch
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

                            // Safely get VERSIONS and ENV_VARS
                            def versions = (config.VERSIONS != null) ? config.VERSIONS.join(", ") : "No Versions Defined"
                            def envVars  = (config.ENV_VARS != null) ? config.ENV_VARS.join(", ") : "No Env Vars Defined"

                            echo "✅ ${branch} → Versions: ${versions} | Env Vars: ${envVars}"

                            // Add to dashboard summary
                            dashboardData << [
                                branch: branch,
                                versions: versions,
                                envVars: envVars
                            ]
                        } else {
                            echo "⚠ ${branch} → Config file not found, skipping..."
                        }
                    }

                    // Save dashboard summary JSON
                    writeJSON file: 'dashboard_summary.json', json: dashboardData, pretty: 4

                    // Archive artifact for Blue Ocean
                    archiveArtifacts artifacts: 'dashboard_summary.json', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo "✅ Dashboard artifact created for all environment branches!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
