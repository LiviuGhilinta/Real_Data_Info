pipeline{
    agent any
    stages{
        stage('Build'){
            steps{
                echo "Building project ..."
                sh '''
                python3 -m venv .venv

                . .venv/bin/activate

                python3 --version
                python3 -m pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest
                echo "Everything is installed! Next Step"
                ''' 
            }
            
        }
        stage('Testing'){
            steps{
                echo "Testing project ..."
                sh '''
                . .venv/bin/activate
                cd ./src
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
    post{
        always{
                sh 'rm -rf .venv'
            }
            
    }
}