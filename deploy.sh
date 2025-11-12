#!/bin/bash
set -e

# === CONFIGURACIÓN ===
PROJECT_ID="professional-task"
REGION="northamerica-south1"
SERVICE_NAME="sentiment-api"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"
SA="945448401729-compute@developer.gserviceaccount.com"
CREDENTIALS_PATH="$HOME/.config/gcloud/service-account.json"

# === EXPORTAR VARIABLE ===
if [ -f "$CREDENTIALS_PATH" ]; then
  export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"
  echo "🔑 Credenciales exportadas desde: $GOOGLE_APPLICATION_CREDENTIALS"
else
  echo "❌ No se encontró el archivo de credenciales en:"
  echo "   $CREDENTIALS_PATH"
  echo "   Crea una clave con:"
  echo "   gcloud iam service-accounts keys create $CREDENTIALS_PATH --iam-account $SA"
  exit 1
fi

# === AUTENTICACIÓN ===
echo "🔧 Autenticando con las credenciales del Service Account..."
gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
gcloud config set project $PROJECT_ID

# === BUILD & DEPLOY ===
echo "🚀 Construyendo imagen con Cloud Build..."
gcloud builds submit --tag $IMAGE


echo "☁️  Desplegando en Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --service-account $SA \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --allow-unauthenticated

echo "✅ Despliegue completado con éxito 🚀"
