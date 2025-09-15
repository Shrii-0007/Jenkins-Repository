def SUMMARY = ""  // Global variable for all branch summaries

pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
    }
    environment {
        DOTNET_ROOT = "/usr/share/dotnet" // Adjust if needed
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
                    def envBranches = ["development","qa","uat","prod","main"]
                    
                    envBranches.each { branch ->
                        // Check if branch exists
                        def status = sh(script: "git ls-remote --heads origin ${branch}", returnStatus: true)
                        if (status == 0) {
                            echo "✅ Found branch: ${branch}"
                            
                            // Fetch branch safely
                            sh "git fetch origin ${branch}:${branch} || echo 'Fetch failed, branch may be empty'"
                            
                            // Checkout appsettings file if exists
                            def configFile = "appsettings.${branch.capitalize()}.json"
                            def appVersion = "N/A"
                            if (sh(script: "git show ${branch}:${configFile}", returnStatus: true) == 0) {
                                sh "git checkout ${branch} -- ${configFile}"
                                def json = readJSON file: configFile
                                appVersion = json?.Version ?: "N/A"
                            }

                            SUMMARY += "Branch: ${branch}, Env: ${branch.capitalize()}, Version: ${appVersion}\n"

                        } else {
                            echo "⚠️ Branch not found: ${branch}, skipping..."
                        }
                    }
                }
            }
        }

        stage('Dotnet Build') {
            steps {
                script {
                    echo "🚀 Building branch: ${env.BRANCH_NAME}"
                    sh 'dotnet restore'
                    sh 'dotnet build -c Release'
                    sh 'dotnet publish -c Release -o ./publish'
                }
            }
        }
    }

    post {
        always {
            echo "📝 Final Branch Summary:\n${SUMMARY}"
        }
        success {
            echo "✅ SUCCESS | Branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Build Failed | Branch: ${env.BRANCH_NAME}"
        }
    }
}
