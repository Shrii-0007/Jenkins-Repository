pipeline {
    agent any
    options { 
        timestamps() 
        skipDefaultCheckout() // ✅ Prevent root checkout to reduce noise
    }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ['Development', 'QA', 'UAT', 'Production']
                    def summary = [:] // To store final summary for all branches

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // ✅ Sparse checkout only the environment JSON file
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [
                                        [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]],
                                        [$class: 'WipeWorkspace'] // Clean folder before checkout
                                    ]
                                ])

                                // ✅ Read JSON quietly
                                def jsonText = sh(script: "cat appsettings.${branch}.json", returnStdout: true).trim()
                                def json = new groovy.json.JsonSlurper().parseText(jsonText)

                                // Extract important fields
                                def appName = json.AppSettings?.AppName ?: "N/A"
                                def version = json.AppSettings?.Version ?: "N/A"
                                def environmentName = json.AppSettings?.Environment ?: "N/A"
                                def extraVar = json.AppSettings?.ExtraVar ?: "N/A"

                                // Store in summary
                                summary[branch] = [AppName: appName, Version: version, Environment: environmentName, ExtraVar: extraVar]

                                // ✅ Clean echo per branch
                                echo "✅ ${branch} → AppName: ${appName}, Version: ${version}, Env: ${environmentName}, ExtraVar: ${extraVar}"
                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                            }
                        }
                    }

                    // ✅ Final consolidated summary for all branches
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
            echo "✅ All environment branches processed in order: Development → QA → UAT → Production" 
        }
        failure { 
            echo "❌ Pipeline failed!" 
        }
    }
}
