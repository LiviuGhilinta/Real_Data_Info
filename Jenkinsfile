pipeline{
    agent any
    stages{
        stage('Build'){
            steps{
                echo "Building project ..."
                sh '''
                python3 --version
                apt install python3-pip
                pip install pytest
                echo "Everything is installed! Next Step"
                ''' 
            }
            
        }
        stage('Testing'){
            steps{
                echo "Testing project ..."
                sh '''
                python3 -m pytest test.py
                '''
            }
            
        }
        stage('Deliver'){
            steps{
                echo "Delivery is not available right now!"
            } 
        }
    }
}