pipeline {
    agent any
    tools {
        nodejs "nodejspkg"
    }
    environment {
        TESTMO_URL = "${TESTMO_URL_PARAM}"
        TESTMO_TOKEN = "${TESTMO_TOKEN_PARAM}"
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building ..'
            }
        }
        stage('Test') {
            environment {
                GIT_SHORT_COMMIT = "${GIT_COMMIT[0..7]}"
            }
            steps {
                // Skip this line if not installing your own Node.js packages
                // sh 'npm ci'

                // Install Testmo CLI tool locally (then use npx testmo .. to run it)
                sh 'npm install --no-save @testmo/testmo-cli'

                // Optionally add a couple of fields such as the
                // git hash and link to the build
                sh '''
                  npx testmo automation:resources:add-field --name git --type string \
                    --value $GIT_SHORT_COMMIT --resources resources.json
                  npx testmo automation:resources:add-link --name build \
                    --url $BUILD_URL --resources resources.json
                '''

                // Run automated tests and report results to Testmo
                sh '''
                  npx testmo automation:run:submit \
                    --instance "$TESTMO_URL" \
                    --project-id 1 \
                    --name "Mocha test run" \
                    --source "unit-tests" \
                    --resources resources.json \
                    --results results/*.xml \
                    -- python3 -m pytest tests --alluredir=../allure_results --junitxml=results/test-results.xml
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying ..'
            }
        }
    }
    post {
        always {
            junit 'results/*.xml'
        }
    }
}