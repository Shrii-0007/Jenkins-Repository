pipeline {
    agent any
    options { timestamps() }

    stages {
        stage('Check out from version control') {
            steps {
                // Standard Jenkins SCM checkout (keeps Git in this stage only)
                checkout scm
            }
        }

        stage('Process Branches') {
            steps {
                script {
                    def branches = ["Development", "QA", "UAT", "Production"]
                    def summary = [:]

                    branches.each { branch ->
                        echo "🌿 Processing Branch: ${branch}"

                        def envs = [
                            "SQL Connection: Server=localhost;Database=SampleDb;User Id=root;Password=;, Logging: Information",
                            "SQL Connection: Server=localhost;Database=SampleDb2;User Id=root;Password=;, Logging: Debug"
                        ]

                        // ✅ Only echo, no sh/cat/git → avoids extra Shell Script tabs
                        echo "✅ ${branch} => • ${envs.join(' • ')}"
                        summary[branch] = envs
                    }

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
