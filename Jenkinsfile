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
                                // Silent checkout (no big git logs)
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "origin/${branch}"]],
                                    userRemoteConfigs: [[
                                        url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                                        credentialsId: 'Github-Credential'
                                    ]],
                                    extensions: [
                                        [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: "appsettings.${branch}.json"]]],
                                        [$class: 'CloneOption', shallow: true, depth: 1, noTags: true, reference: '', timeout: 10, quiet: true]
                                    ]
                                ])

                                // Read JSON file without printing it
                                def json = new groovy.json.JsonSlurper().parseText(
                                    readFile("appsettings.${branch}.json")
                                )

                                def versions = json.AppSettings?.Version ?: "N/A"
                                def envs     = json.AppSettings?.Environment ?: "N/A"
                                def extras   = json.AppSettings?.ExtraVar ?: "N/A"

                                // 🎯 Only clean block will be shown in Jenkins dashboard
                                echo """
----------------------------------------
📌 Branch: ${branch}
   Environment : ${envs}
   Version     : ${versions}
   Variables   : ${extras}
----------------------------------------
"""
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
