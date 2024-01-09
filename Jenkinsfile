pipeline {
    agent any
          // Tried to create docker env but got docker command not recognised error
//        docker {
//            image 'python:3.10-slim'
//        }
//    }

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
                 
                 sh 'docker build -t panelsearch .'
//                 sh 'docker run -i -t panelsearch'
            }
        }
        
        stage('Test') {
            steps {
                // Run tests
                echo 'Testing..'
                
                withPythonEnv('python3') {
                    sh 'pip install pytest'
                    sh 'pytest'
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
