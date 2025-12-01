pipeline {
    agent any

    stages {
        stage('Checkout code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t sentiment-api:jenkins .'
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
