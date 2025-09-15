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
                            def versions = config.VERSIONS.join(", ")
                            def envVars = config.ENV_VARS.join(", ")

                            echo "✅ ${branch} → Versions: ${versions} | Env Vars: ${envVars}"

                            // Add branch info to dashboard data
                            dashboardData << [
                                branch: branch,
                                versions: versions,
                                envVars: envVars
                            ]
                        } else {
                            echo "⚠ ${branch} → Config file not found, skipping..."
                        }
                    }

                    // Write dashboard summary JSON
                    writeJSON file: 'dashboard_summary.json', json: dashboardData, pretty: 4

                    // Archive artifact for Blue Ocean
                    archiveArtifacts artifacts: 'dashboard_summary.json', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo "✅ Dashboard artifact created for all branches!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
