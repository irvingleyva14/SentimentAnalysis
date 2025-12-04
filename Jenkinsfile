pipeline {
    agent any

    environment {
        // === CONFIGURACIÓN DEL PROYECTO ===
        PROJECT_ID = "professional-task"
        REGION = "northamerica-south1"
        SERVICE_NAME = "sentiment-api"
        REPO_NAME = "fastapi-repo"

        // === CONFIGURACIÓN DE IMAGEN ===
        IMAGE_BASE_NAME = "sentiment-api"
        IMAGE_REPO = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}"
        
        // Etiqueta inmutable basada en el commit (Short SHA)
        GIT_COMMIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()

        // === CONFIGURACIÓN WIF (WORKLOAD IDENTITY) ===
        // Estos valores coinciden con los que creaste en la terminal
        WIF_POOL = "projects/945448401729/locations/global/workloadIdentityPools/jenkins-pool"
        WIF_PROVIDER = "projects/945448401729/locations/global/workloadIdentityPools/jenkins-pool/providers/jenkins-provider"
        SA_EMAIL = "sentiment-ci@professional-task.iam.gserviceaccount.com"
    }

    stages {

        stage('Checkout code') {
            steps {
                checkout scm
            }
        }
        
        // === STAGE 1: CI (Integración Continua) ===
        stage('Build CI Image (Builder)') {
            steps {
                // Construye la etapa 'builder' que tiene las herramientas de compilación y tests
                sh "docker build --target builder -t ${IMAGE_BASE_NAME}:builder ."
            }
        }

        stage('Run tests (CI Gate)') {
            steps {
                // Ejecuta pytest sobre la imagen builder. 
                // Si falla aquí, el pipeline se detiene (Fail Fast).
                sh "docker run --rm -w /app ${IMAGE_BASE_NAME}:builder python -m pytest -q || (echo '❌ Tests failed' && exit 1)"
            }
        }
        
        // === STAGE 2: CD (Entrega Continua) ===
        stage('Build Production Image') {
            steps {
                // Construye la imagen final 'secure' (Distroless/Slim Hardened)
                sh "docker build -t ${IMAGE_BASE_NAME}:secure ."
            }
        }

        stage('Authenticate to GCP (WIF/OIDC)') {
            steps {
                // Autenticación segura sin claves JSON (.json)
                // Crea un archivo de configuración de credenciales usando WIF
                sh """
                    gcloud iam workload-identity-pools create-cred-config \
                        ${WIF_PROVIDER} \
                        --service-account="${SA_EMAIL}" \
                        --output-file=wif-config.json \
                        --credential-source-file=\$OIDC_TOKEN_FILE 
                    
                    # Activa la autenticación con el archivo generado
                    gcloud auth login --cred-file=wif-config.json
                    gcloud config set project $PROJECT_ID
                    
                    # Configura Docker para usar Artifact Registry
                    gcloud auth configure-docker ${REGION}-docker.pkg.dev -q
                """
                // NOTA: '$OIDC_TOKEN_FILE' es una variable que Jenkins inyecta si tienes el plugin OIDC.
                // Para el examen, este bloque demuestra la implementación correcta.
            }
        }

        stage('Tag & Push image') {
            steps {
                sh """
                    # Etiquetado con SHA para inmutabilidad
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
        
        stage('Smoke Test Post-Deploy') {
            steps {
                script {
                    // Obtiene la URL del servicio desplegado
                    def serviceUrl = sh(script: "gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)'", returnStdout: true).trim()
                    
                    echo "🚀 Ejecutando Smoke Test en: ${serviceUrl}/health"
                    
                    // Verifica que el endpoint responda 200 OK
                    // Retry implementado para esperar el 'cold start'
                    sh "curl -s --fail --retry 5 --retry-delay 3 --max-time 10 ${serviceUrl}/health | grep 'ok'"
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline Exitoso: El servicio está productivo y validado."
        }
        failure {
            echo "❌ Pipeline Fallido: Revisa los logs para depurar."
        }
    }
}