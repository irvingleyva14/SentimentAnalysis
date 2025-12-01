pipeline {
    agent any

    environment {
        // Datos de GCP / Cloud Run / Artifact Registry
        PROJECT_ID = "professional-task"
        REGION = "northamerica-south1"
        SERVICE_NAME = "sentiment-api"
        REPO_NAME = "fastapi-repo"

        // Ruta completa del repositorio de imágenes en Artifact Registry
        IMAGE_REPO = "northamerica-south1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}"

        // Credencial de GCP (ID del Secret File en Jenkins)
        GCP_SA_KEY = credentials('gcp-service-account')
    }

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

        stage('Run tests inside container') {
            steps {
                sh 'docker run --rm sentiment-api:jenkins pytest -q || (echo "Tests failed" && exit 1)'
            }
        }

        stage('Authenticate to GCP') {
            steps {
                sh """
                    gcloud auth activate-service-account --key-file=$GCP_SA_KEY
                    gcloud config set project $PROJECT_ID
                    gcloud auth configure-docker northamerica-south1-docker.pkg.dev -q
                """
            }
        }

        stage('Tag & Push image to Artifact Registry') {
            steps {
                sh """
                    docker tag sentiment-api:jenkins $IMAGE_REPO:${BUILD_NUMBER}
                    docker push $IMAGE_REPO:${BUILD_NUMBER}
                """
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                sh """
                    gcloud run deploy $SERVICE_NAME \
                      --image $IMAGE_REPO:${BUILD_NUMBER} \
                      --region $REGION \
                      --platform managed \
                      --allow-unauthenticated \
                      --service-account=sentiment-ci@${PROJECT_ID}.iam.gserviceaccount.com \
                      --set-env-vars BUCKET_NAME=model-senti-analy-ia
                """
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline COMPLETO: build + tests + push + deploy ok"
        }
        failure {
            echo "❌ Pipeline falló. Revisar el log de la etapa correspondiente."
        }
    }
}
