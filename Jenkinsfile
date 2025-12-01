pipeline {
    agent any

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-service-account')
    }

    stages {
        stage('Checkout code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                sh '''
                sudo usermod -aG docker jenkins
                docker build -t sentiment-api:jenkins .
                '''
            }
        }
    }

    post {
        success {
            echo "🚀 Build completado con éxito"
        }
        failure {
            echo "❌ Build fallido"
        }
    }
}
