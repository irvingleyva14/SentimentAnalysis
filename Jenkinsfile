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
                    def serviceUrl = sh(script: "gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)'", returnStdout: true).trim()
                    echo "🚀 URL del Servicio: ${serviceUrl}"
                    
                    // Aumentamos la espera inicial a 30s por el modelo pesado
                    echo "⏳ Esperando 30 segundos para carga del modelo en Cold Start..."
                    sleep 30
                    
                    echo "🔄 Iniciando intentos de conexión..."
                    // Bucle de reintento manual (más robusto que curl --retry para 503s de inicio)
                    // Intenta durante 2 minutos (12 intentos * 10s)
                    def isAlive = false
                    for (int i = 0; i < 12; i++) {
                        // El comando devuelve 0 (true) si grep encuentra 'status', o falla
                        // Usamos '|| true' para que el script no muera si curl falla
                        def status = sh(script: "curl -s ${serviceUrl}/health | grep 'status'", returnStatus: true)
                        
                        if (status == 0) {
                            echo "✅ Intento ${i+1}: ÉXITO. El servicio respondió."
                            isAlive = true
                            break
                        } else {
                            echo "⚠️ Intento ${i+1}: Falló (posible 503/Cold Start). Reintentando en 10s..."
                            sleep 10
                        }
                    }
                    
                    if (!isAlive) {
                        echo "❌ Smoke Test FALLIDO: El servicio no respondió después de varios intentos."
                        error("Deployment verification failed: Service unreachable")
                    } else {
                        echo "✅ Smoke Test COMPLETADO."
                    }
                }
            }
        }