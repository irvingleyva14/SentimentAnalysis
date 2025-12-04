pipeline {
    agent any

    environment {
        // === DATOS DEL PROYECTO ===
        PROJECT_ID = "professional-task"
        REGION = "northamerica-south1"
        SERVICE_NAME = "sentiment-api"
        REPO_NAME = "fastapi-repo"

        // === RUTAS E IMAGEN ===
        IMAGE_BASE_NAME = "sentiment-api"
        IMAGE_REPO = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}"
        
        // Etiqueta inmutable (Short SHA)
        GIT_COMMIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()

        // === CREDENCIALES ===
        GCP_SA_KEY = credentials('gcp-service-account')
        SA_EMAIL = "sentiment-ci@professional-task.iam.gserviceaccount.com"
    }

    stages {

        stage('Checkout code') {
            steps {
                checkout scm
            }
        }
        
        // --- CI STAGES ---
        stage('Build CI Image (Builder)') {
            steps {
                sh "docker build --target builder -t ${IMAGE_BASE_NAME}:builder ."
            }
        }

        stage('Run tests (CI Gate)') {
            steps {
                // Inyectamos PYTHONPATH para que encuentre los paquetes
                sh "docker run --rm -w /app -e PYTHONPATH=/app/site-packages ${IMAGE_BASE_NAME}:builder python -m pytest -q || (echo '❌ Tests failed' && exit 1)"
            }
        }
        
        // --- CD STAGES ---
        stage('Build Production Image') {
            steps {
                sh "docker build -t ${IMAGE_BASE_NAME}:secure ."
            }
        }

        stage('Authenticate to GCP') {
            steps {
                sh """
                    gcloud auth activate-service-account --key-file=$GCP_SA_KEY
                    gcloud config set project $PROJECT_ID
                    gcloud auth configure-docker ${REGION}-docker.pkg.dev -q
                """
            }
        }

        stage('Tag & Push image') {
            steps {
                sh """
                    docker tag ${IMAGE_BASE_NAME}:secure ${IMAGE_REPO}:${GIT_COMMIT_SHA}
                    docker push ${IMAGE_REPO}:${GIT_COMMIT_SHA}
                    echo "✅ Imagen subida: ${IMAGE_REPO}:${GIT_COMMIT_SHA}"
                """
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                sh """
                    gcloud run deploy $SERVICE_NAME \
                      --image ${IMAGE_REPO}:${GIT_COMMIT_SHA} \
                      --region $REGION \
                      --platform managed \
                      --allow-unauthenticated \
                      --service-account=${SA_EMAIL} \
                      --memory=1Gi --cpu=1 \
                      --min-instances=0 \
                      --set-env-vars ENVIRONMENT=production
                """
            }
        }
        
        // --- VALIDACIÓN ---
        stage('Smoke Test Post-Deploy') {
            steps {
                script {
                    def serviceUrl = sh(script: "gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)'", returnStdout: true).trim()
                    echo "🚀 URL del Servicio: ${serviceUrl}"
                    
                    echo "⏳ Esperando 30 segundos iniciales para Cold Start..."
                    sleep 30
                    
                    def isAlive = false
                    // Bucle de reintentos (12 intentos x 10s = 2 minutos)
                    for (int i = 1; i <= 12; i++) {
                        echo "🔄 Intento ${i}/12..."
                        // Usamos returnStatus: true para que no falle el script si curl da error 503
                        def status = sh(script: "curl -s --fail ${serviceUrl}/health | grep 'ok'", returnStatus: true)
                        
                        if (status == 0) {
                            echo "✅ ¡ÉXITO! El servicio respondió 'ok'."
                            isAlive = true
                            break
                        } else {
                            echo "⚠️ Aún no responde (posible 503). Esperando 10s..."
                            sleep 10
                        }
                    }
                    
                    if (!isAlive) {
                        error("❌ Smoke Test FALLIDO: El servicio no respondió después de 2 minutos.")
                    }
                }
            }
        }
    } // Cierre de stages

    post {
        success {
            echo "🏆 PIPELINE COMPLETADO EXITOSAMENTE 🏆"
        }
        failure {
            echo "❌ El pipeline falló. Revisa los logs."
        }
    } // Cierre de post
} // Cierre de pipeline