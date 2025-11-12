# Decisiones técnicas clave

## Elección de FastAPI
- Se seleccionó **FastAPI** por su rendimiento, tipado fuerte y soporte nativo para OpenAPI/Swagger.

## Elección del modelo
- Se usa `tabularisai/multilingual-sentiment-analysis` de **Hugging Face** por su soporte multilingüe.

## Carga del modelo
- Inicialmente, el modelo se descargaba en cada request (versión lenta).
- Luego se aplicó un patrón **singleton**, cargando el modelo solo una vez.
- Finalmente, se optimizó la carga desde un **bucket GCS**, evitando descargas repetitivas.

## Despliegue
- Se eligió **Google Cloud Run** por su escalabilidad automática, simplicidad y facturación por uso.
- El despliegue se automatiza con `deploy.sh`, que:
  1. Construye la imagen Docker.
  2. La sube a Artifact Registry.
  3. Actualiza el servicio en Cloud Run.

## Contenerización
- Se usa una imagen base ligera (`python:3.11-slim`).
- Se exponen los puertos 8000 local y 8080 en Cloud Run.
- El comando de ejecución final es `CMD ["python", "run.py"]`.

## Razón de configuración del puerto
- Cloud Run exige que el contenedor escuche en el puerto **8080** definido en `$PORT`.
- Por eso, el `run.py` usa:
  ```python
  uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
