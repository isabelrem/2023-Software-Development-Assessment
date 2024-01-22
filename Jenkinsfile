pipeline {
    agent any
          // Tried to create docker env but got docker command not recognised error
//        docker {
//            image 'python:3.10-slim'
//        }
//    }
//        docker {
//              image "docker:24.0.6-git"
//          } 
    agent { dockerfile true}

    stages {
        stage('Build') {
            steps {
                // Build the project
                echo 'Building..'
                
                // Tried to create conda env but got wget command not recognised error 
 //               sh '''#!/usr/bin/env bash
 //                   wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -nv -O miniconda.sh
 //                   bash miniconda.sh -b -p $WORKSPACE/miniconda
 //                   conda config --set always_yes yes --set changeps1 no
 //                   conda update -q conda
 //                   
 //                   conda env create -f environment.yaml
 //                   
 //                   pip install -r requirements.txt
 //               '''
                 // Checkout the source code from the configured source code management system
                 checkout scm 
//                 sh 'docker build -t panelsearch .'
//                 sh 'docker run -i -t panelsearch'
                 sh 'docker system prune --all --volumes --force' // Remove unused Docker resources
                 sh './setup.sh'
            }
        }
        
        stage('Test') {
            steps {
                // Run tests
                echo 'Testing..'
                
                withPythonEnv('python3') {
                    sh 'pip install pytest'
                    sh 'pip install -r requirements.txt'
                    sh 'pytest'
                }
                
                script {
                    sh 'docker ps' // List running Docker containers
                    def connectionSuccessful = false
                    
                    for (int attempt = 1; attempt <= 5; attempt++) {
                        echo "Attempt $attempt to connect to the database..."
                        def exitCode = sh(script: '''
                            ./setup.sh
                        ''', returnStatus: true)

                        if (exitCode == 0) {
                            connectionSuccessful = true
                            echo "Connected successfully! Running pytest..."

                            // Run pytest
                            sh 'docker exec panelsearch pytest tests/'

                            // Check for test failures in the captured output
                            if (currentBuild.rawBuild.getLog(2000).join('\n').contains("test summary info") && currentBuild.rawBuild.getLog(2000).join('\n').contains("FAILED")) {
                                failure(message:"Pytest completed with test failures")
                            }

                            // Check the Jenkins console log for pytest exit code
                            def pytestExitCode = currentBuild.rawBuild.getLog(2000).find { line -> line =~ /.*Pytest exit code: (\d+).*/ }
                            if (pytestExitCode) {
                                pytestExitCode = Integer.parseInt(pytestExitCode.replaceAll(/.*Pytest exit code: (\d+).*/, '$1'))
                                if (pytestExitCode != 0) {
                                    failure(message:"Pytest failed with exit code $pytestExitCode")
                                }
                            }
                            break
                        }

                        echo "Connection failed. Waiting for 60 seconds before the next attempt..."
                        sleep 60
                    }

                    if (!connectionSuccessful) {
                        failure(message:"All connection attempts failed. Exiting...")
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // Deploy build
                echo 'Deploying....'
            }
        }
    }
    
    post {
        always{// This ensures cleanup is executed regardless of build outcome
            script {
                // Cleanup Docker
                sh 'docker stop panelsearch'
                sh 'docker rm panelsearch'
                sh 'docker stop panelsearch-database'
                sh 'docker rm panelsearch-database'
                sh 'docker system prune --all --volumes --force'
            }
        }
            
        success {
            // This block is executed if the pipeline runs successfully.
            echo 'Pipeline succeeded! Your project is built and tested.'
        }
        
        failure {
            // This block is executed if the pipeline fails.
            echo 'Pipeline failed. Please check the logs for details.'
        }
    }
}
