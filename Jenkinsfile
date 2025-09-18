import groovy.json.JsonSlurper

pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process Branches') {
            steps {
                script {
                    def branches = ["Development", "QA", "UAT", "Production"]
                    def summary = [:]

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        dir("tmp_${branch}") {
                            try {
                                // Checkout only appsettings.<branch>.json
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [[$class: 'SparseCheckoutPaths',
                                                  sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]]]
                                ])

                                // Read and parse JSON
                                def jsonText = readFile("appsettings.${branch}.json")
                                def json = new JsonSlurper().parseText(jsonText)

                                def envs = []
                                json.AppSettings.each { app ->
                                    app.Settings.each { s ->
                                        def sqlConn = s.Dev_MySql_Connection_String ?: "N/A"
                                        def logging = s.Logging ?: "N/A"
                                        envs << "SQL Connection: ${sqlConn}, Logging: ${logging}"
                                    }
                                }

                                // Print branch output in your style
                                echo "✅ ${branch} => • ${envs.join(' • ')}"

                                summary[branch] = envs

                            } catch (Exception e) {
                                echo "⚠ ${branch} → Config file not found or branch missing"
                            }
                        }
                    }

                    // Final Summary
                    echo "📊 Final Summary (All Branches):"
                    summary.each { br, vals ->
                        echo "📂 ${br} Results: • ${vals.join(' • ')}"
                    }

                    echo "✅ All environment branches processed in order: Development → QA → UAT → Production"
                }
            }
        }
    }
}
