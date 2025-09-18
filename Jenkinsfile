pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Process All Environment Branches') {
            steps {
                script {
                    def branches = ["Development", "QA", "UAT", "Production"]
                    def summary = [:]

                    branches.each { branch ->
                        dir("tmp_${branch}") {
                            checkout([$class: 'GitSCM',
                                branches: [[name: "*/${branch}"]],
                                doGenerateSubmoduleConfigurations: false,
                                extensions: [[$class: 'WipeWorkspace']],
                                userRemoteConfigs: [[
                                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                    credentialsId: 'Github-Credential'
                                ]]
                            ])

                            def configFile = "appsettings.${branch}.json"

                            // 👇 use shell instead of readFile (Blue Ocean won't add tab)
                            def content = sh(script: "cat ${configFile}", returnStdout: true).trim()
                            def envs = content.readLines().findAll { it.trim() }
                            summary[branch] = envs

                            // ✅ Only clean branch summary log (no checkout/log noise)
                            echo "✅ ${branch} =>"
                            envs.each { e ->
                                echo "    • ${e}"
                            }
                        }
                    }

                    echo ""
                    echo "📊 Final Summary (All Branches):"
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
}
