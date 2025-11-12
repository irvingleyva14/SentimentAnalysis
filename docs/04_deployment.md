# Guía de despliegue

## 1️⃣ Requisitos previos

 Tener configurado `gcloud` y haber ejecutado:

  gcloud auth login
  gcloud config set project professional-task

## 2️⃣ Despliegue local con Docker

  docker build -t sentiment-api .
  docker run -p 8080:8080 sentiment-api

Verifica en: http://localhost:8080/docs

## 3️⃣ Despliegue en Cloud Run

El script deploy.sh automatiza el proceso:

./deploy.sh

Internamente realiza:

1. Construcción de la imagen.

2. Subida a Artifact Registry.

3. Actualización del servicio en Cloud Run.

Ejemplo de comando base:

gcloud run deploy sentiment-api \
  --image=us-docker.pkg.dev/professional-task/sentiment-repo/sentiment-api \
  --region=northamerica-south1 \
  --platform=managed \
  --allow-unauthenticated

##  4️⃣ Mantenimiento y limpieza

Para eliminar imágenes antiguas:

gcloud artifacts docker images delete \
  us-docker.pkg.dev/professional-task/sentiment-repo/sentiment-api@<digest>

O para borrar todas las versiones viejas automáticamente:

gcloud artifacts docker images list us-docker.pkg.dev/professional-task/sentiment-repo/sentiment-api \
  --format="get(version)" | xargs -I {} gcloud artifacts docker images delete {} --quiet

## 5️⃣ Costos y buenas prácticas

Cloud Run cobra solo por invocaciones y tiempo activo.

Artifact Registry cobra por almacenamiento de imágenes.

GCS cobra por tamaño almacenado.

💡 Recomendaciones:

Pausar el servicio cuando no se use:

gcloud run services update sentiment-api --no-traffic

* Eliminar imágenes y revisiones obsoletas.

* Mantener solo la última versión desplegada.