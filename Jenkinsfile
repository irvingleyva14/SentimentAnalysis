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
        
        // Etiqueta inmutable (Short SHA del commit)
        GIT_COMMIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()

        // === CREDENCIALES ===
        // Usamos la clave para garantizar que pase AHORA MISMO. 
        // (En un entorno real con plugin OIDC, usaríamos la lógica WIF).
        GCP_SA_KEY = credentials('gcp-service-account')
        SA_EMAIL = "sentiment-ci@professional-task.iam.gserviceaccount.com"
    }

    stages {

        stage('Checkout code') {
            steps {
                checkout scm
            }
        }
        
        // ----------------------------------------------------
        // FASE 1: INTEGRACIÓN CONTINUA (CI)
        // ----------------------------------------------------
        stage('Build CI Image (Builder)') {
            steps {
                // Construimos el target 'builder' que tiene las herramientas de test
                sh "docker build --target builder -t ${IMAGE_BASE_NAME}:builder ."
            }
        }

        stage('Run tests (CI Gate)') {
            steps {
                // Ejecutamos pytest sobre la imagen builder.
                // IMPORTANTE: Inyectamos PYTHONPATH para que encuentre las dependencias.
                sh "docker run --rm -w /app -e PYTHONPATH=/app/site-packages ${IMAGE_BASE_NAME}:builder python -m pytest -q || (echo '❌ Tests failed' && exit 1)"
            }
        }
        
        // ----------------------------------------------------
        // FASE 2: ENTREGA CONTINUA (CD)
        // ----------------------------------------------------
        stage('Build Production Image') {
            steps {
                // Construimos la imagen final 'secure' (Distroless/Slim Hardened)
                sh "docker build -t ${IMAGE_BASE_NAME}:secure ."
            }
        }

        stage('Authenticate to GCP') {
            steps {
                sh """
                    # Activamos la Service Account
                    gcloud auth activate-service-account --key-file=$GCP_SA_KEY
                    
                    # Configuramos proyecto y Docker
                    gcloud config set project $PROJECT_ID
                    gcloud auth configure-docker ${REGION}-docker.pkg.dev -q
                """
            }
        }

        stage('Tag & Push image') {
            steps {
                sh """
                    # Etiquetado inmutable para trazabilidad
                    docker tag ${IMAGE_BASE_NAME}:secure ${IMAGE_REPO}:${GIT_COMMIT_SHA}
                    docker push ${IMAGE_REPO}:${GIT_COMMIT_SHA}
                    echo "✅ Imagen subida a Artifact Registry: ${GIT_COMMIT_SHA}"
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
        
        // ----------------------------------------------------
        // FASE 3: VALIDACIÓN POST-DESPLIEGUE
        // ----------------------------------------------------
        stage('Smoke Test Post-Deploy') {
            steps {
                script {
                    // 1. Obtener la URL del servicio
                    def serviceUrl = sh(script: "gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)'", returnStdout: true).trim()
                    
                    echo "🚀 URL del Servicio: ${serviceUrl}"
                    echo "⏳ Esperando 15 segundos para 'Cold Start' de Cloud Run..."
                    sleep 15
                    
                    // 2. Ejecutar prueba de salud (Healthcheck)
                    // Usamos 'grep status' porque el JSON de respuesta es {"status": "ok"}
                    try {
                        sh "curl -s --fail --show-error ${serviceUrl}/health | grep 'status'"
                        echo "✅ Smoke Test EXITOSO: El servicio responde correctamente."
                    } catch (Exception e) {
                        echo "❌ Smoke Test FALLIDO: El endpoint /health no respondió 200 OK o el JSON esperado."
                        error("Deployment verification failed")
                    }
                }
            }
        }
    }

    post {
        success {
            echo "🏆 PIPELINE COMPLETADO EXITOSAMENTE 🏆"
        }
        failure {
            echo "❌ El pipeline falló. Revisa los logs."
        }
    }
}