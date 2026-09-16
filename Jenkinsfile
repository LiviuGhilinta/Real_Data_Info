pipeline{
    agent any
    stages{
        stage('Build'){
            echo "Building project ..."
            sh '''
            python3 --version
            pip install -r requirements.txt
            echo "Everything is installed! Next Step"
            ''' 
        }
        stage('Testing'){
            echo "Testing project ..."
            sh '''
            python3 test.py
            '''
        }
        stage('Deliver'){
            echo "Delivery is not available right now!"
        }
    }
}