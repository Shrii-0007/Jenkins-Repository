pipeline {
    agent any

    stages {
        stage('Checkout Branch') {
            steps {
                script {
                    // Get all remote branches
                    def branches = sh(script: "git ls-remote --heads https://github.com/Shrii-0007/Jenkins-Repository.git | awk '{print \$2}' | sed 's#refs/heads/##'", returnStdout: true).trim().split("\n")

                    for (b in branches) {
                        echo "🌿 Processing branch: ${b}"

                        // Checkout the branch
                        sh "git fetch origin ${b}:${b}"
                        sh "git checkout ${b}"

                        def configFile = "appsettings.json"
                        if (!fileExists(configFile)) {
                            echo "⚠️ Config file not found in branch ${b}, skipping..."
                            continue
                        }

                        def config = readJSON file: configFile
                        env.APP_NAME = config.AppSettings.AppName
                        env.VERSION = config.AppSettings.Version
                        env.ENVIRONMENT = config.AppSettings.Environment
                        env.EXTRA_VAR = config.AppSettings.ExtraVar

                        echo "📝 Branch: ${b} | AppName: ${env.APP_NAME} | Version: ${env.VERSION} | Environment: ${env.ENVIRONMENT}"
                    }
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                script {
                    echo "🚀 Build & Deploy logic goes here"
                    // Real build/deploy commands here
                }
            }
        }
    }

    post {
        always {
            echo "📊 Blue Ocean Dashboard: Display branch-wise info above"
        }
    }
}
