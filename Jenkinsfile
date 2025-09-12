pipeline {
    agent any

    environment {
        ENV_NAME = "Development"
        BRANCH_NAME = "Development"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Development',
                    url: 'https://github.com/Shrii-0007/Jenkins-Repository.git',
                    credentialsId: 'Github-Credential'
            }
        }

        stage('Build') {
            steps {
                echo "Running build for DEVELOPMENT branch"
                sh 'echo "Build commands for DEVELOPMENT branch"'
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running unit tests for DEVELOPMENT branch"
                sh 'echo "Unit test commands for DEVELOPMENT branch"'
            }
        }

        stage('Dependency Change Report') {
            steps {
                sh '''
                set +e
                echo "===== Dependency Change Report =====" > report.txt
                echo "Branch: ${BRANCH_NAME}" >> report.txt
                git log -1 --pretty=format:"%h - %an : %s" >> report.txt
                echo "" >> report.txt

                commit_count=$(git rev-list --count HEAD 2>/dev/null | wc -l)
                if [ "$commit_count" -lt 2 ]; then
                    echo "Not enough commits to compare (first commit on branch)." >> report.txt
                    exit 0
                fi

                for file in package.json requirements.txt pom.xml build.gradle; do
                    if [ -f "$file" ]; then
                        echo "--- $file changes ---" >> report.txt
                        git diff HEAD~1 HEAD -- "$file" >> report.txt
                    else
                        echo "$file not found" >> report.txt
                    fi
                done

                csproj_files=$(ls *.csproj 2>/dev/null | wc -l)
                if [ "$csproj_files" -gt 0 ]; then
                    echo "--- .csproj changes ---" >> report.txt
                    git diff HEAD~1 HEAD -- *.csproj >> report.txt
                else
                    echo ".csproj file not found" >> report.txt
                fi
                '''
            }
        }

        stage('Environment Variables Report') {
            steps {
                script {
                    def envText = ""
                    env.each { key, value -> envText += "${key} = ${value}\n" }
                    writeFile file: 'env_report.txt', text: envText
                }
            }
        }

        stage('Console Preview of Reports') {
            steps {
                echo "===== DISPLAY: Dependency + Environment Reports ====="
                sh '''
                if [ -f report.txt ]; then cat report.txt; fi
                if [ -f env_report.txt ]; then cat env_report.txt; fi
                '''
                echo "===== END OF REPORTS ====="
            }
        }

        stage('Publish Reports') {
            steps {
                archiveArtifacts artifacts: 'report.txt, env_report.txt', fingerprint: true
            }
        }
    }
}
