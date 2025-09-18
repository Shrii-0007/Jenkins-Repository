pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout() // ✅ Disable root checkout to avoid extra Blue Ocean tabs
    }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ["Development", "QA", "UAT", "Production"]
                    def summary = [:]

                    branches.each { branch ->
                        dir("tmp_${branch}") {
                            // ✅ Explicit checkout per branch
                            checkout([$class: 'GitSCM',
                                branches: [[name: "*/${branch}"]],
                                doGenerateSubmoduleConfigurations: false,
                                extensions: [[$class: 'WipeWorkspace']],
                                userRemoteConfigs: [[
                                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                    credentialsId: 'Github-Credential'
                                ]]
                            ])

                            // ✅ Read file using shell to avoid extra readFile tab
                            def content = sh(
                                script: "cat appsettings.${branch}.json",
                                returnStdout: true
                            ).trim()

                            def envs = content.readLines().findAll { it.trim() }
                            summary[branch] = envs

                            // ✅ Branch summary only
                            echo "🌿 ${branch} =>"
                            envs.each { e ->
                                echo "    • ${e}"
                            }
                        }
                    }

                    // ✅ Final summary for all branches
                    echo "\n📊 Final Summary (All Branches):"
                    summary.each { br, vals ->
                        echo "📂 ${br} Results:"
                        vals.each { e ->
                            echo "    • ${e}"
                        }
                        echo ""
                    }

                    echo "✅ All environment branches processed in order: Development → QA → UAT → Production"
                }
            }
        }
    }

    post {
        always {
            echo "🔔 Build finished. GitHub notified of status."
        }
    }
}
