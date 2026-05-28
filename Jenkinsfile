pipeline {
    agent any

    environment {
        IMAGE_NAME = 'taskflow-api'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKERHUB_PASS = credentials('dockerhub-password')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m pip install -r app/requirements.txt
                    python3 -m pytest app/test_main.py -v
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG -t $DOCKERHUB_USER/$IMAGE_NAME:latest .'
            }
        }

        stage('Push') {
            when { branch 'main' }
            steps {
                sh '''
                    echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:latest
                    docker logout
                '''
            }
        }

        stage('Deploy local') {
            when { branch 'main' }
            steps {
                sh '''
                    cp .env.example .env
                    docker compose up -d --build app
                '''
            }
        }
    }
}
