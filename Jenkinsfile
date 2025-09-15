pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
    }
    environment {
        DOTNET_ROOT = "/usr/share/dotnet" // Adjust if needed
        SUMMARY = ""
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
                    // List of environment branches
                    def envBranches = ["development","qa","uat","prod","main"]
                    
                    envBranches.each { branch ->
                        // Check if branch exists
                        def status = sh(script: "git ls-remote --heads origin ${branch}", returnStatus: true)
                        if (status == 0) {
                            echo "✅ Found branch: ${branch}"
                            
                            // Fetch branch
                            sh "git fetch origin ${branch}:${branch}"
                            
                            // Checkout appsettings
                            sh "git checkout ${branch} -- appsettings.${branch.capitalize()}.json || echo 'No appsettings found'"
                            
                            // Read appsettings JSON
                            def appEnv = branch.capitalize()
                            def appVersion = "N/A"
                            def configFile = "appsettings.${appEnv}.json"
                            if (fileExists(configFile)) {
                                def json = readJSON file: configFile
                                appVersion = json?.Version ?: "N/A"
                            }
                            
                            // Append summary for Blue Ocean
                            SUMMARY += "Branch: ${branch}, Env: ${appEnv}, Version: ${appVersion}\n"
                            
                        } else {
                            echo "⚠️ Branch not found on remote: ${branch}, skipping..."
                        }
                    }
                }
            }
        }

        stage('Dotnet Build') {
            steps {
                script {
                    // Only build for main or other active branch
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
