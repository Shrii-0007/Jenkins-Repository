pipeline {
    agent any
    options { 
        timestamps()
        skipDefaultCheckout()
    }

    stages {
        stage('Discover and Process Environment Branches') {
            steps {
                script {
                    // 1️⃣ Fetch all remote branches
                    def remoteBranches = sh(
                        script: 'git ls-remote --heads https://github.com/Shrii-0007/Jenkins-Repository.git',
                        returnStdout: true
                    ).trim().split("\n")
                     .collect { it.split()[1].replace('refs/heads/', '') }

                    echo "🌿 Remote branches found: ${remoteBranches}"

                    // 2️⃣ Filter only environment branches (optional: regex)
                    def envBranches = remoteBranches.findAll { it =~ /^(Development|QA|UAT|Production)$/ }

                    def summary = [:]

                    // 3️⃣ Process each branch
                    envBranches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // Checkout only the JSON file
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [
                                        [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]],
                                        [$class: 'WipeWorkspace']
                                    ]
                                ])

                                // Read JSON file
                                def jsonText = sh(script: "cat appsettings.${branch}.json", returnStdout: true).trim()
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def version = json.AppSettings?.Version ?: "N/A"
                                def environmentName = json.AppSettings?.Environment ?: branch
                                def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                                summary[branch] = [AppName: appName, Version: version, Environment: environmentName, ExtraVar: extraVar]

                                echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file missing or branch issue"
                            }
                        }
                    }

                    // 4️⃣ Print final summary
                    echo "\n📊 Final Summary (All Branches):"
                    summary.each { br, vals ->
                        echo "📂 ${br}: AppName=${vals.AppName}, Version=${vals.Version}, Env=${vals.Environment}, ExtraVar=${vals.ExtraVar}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ All environment branches processed dynamically"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
