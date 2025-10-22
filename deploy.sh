#!/bin/bash

PROJECT_ID=professional-task
SERVICE_NAME=sentiment-api
REGION=us-central1
IMAGE=gcr.io/$PROJECT_ID/$SERVICE_NAME

echo "🔨 Construyendo imagen con Docker..."
docker build -t $IMAGE .

echo "🚀 Subiendo imagen a Container Registry..."
docker push $IMAGE

echo "☁️ Desplegando en Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --concurrency 1

echo "✅ Despliegue completo!"
