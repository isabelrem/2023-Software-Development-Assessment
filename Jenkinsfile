pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // Build the project
                echo 'Building..'
                sh 'conda env create -f environment.yaml'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                // Run tests
                echo 'Testing..'
                sh 'pytest'
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
