# app/services/model_loader.py
from transformers import pipeline
from app.core.logger import setup_logger
from google.cloud import storage
from pathlib import Path
import os
import time

logger = setup_logger(__name__)

class ModelLoader:
    """Carga el modelo desde local o GCS (sin archivos comprimidos)."""

    def __init__(
        self,
        model_path: str = "models/multilingual-sentiment",
        bucket_name: str = "model-senti-analy-ia",
        prefix: str = "models/multilingual-sentiment"
    ):
        self.model_path = Path(model_path)
        self.bucket_name = bucket_name
        self.prefix = prefix
        self._pipeline = None

    def _download_from_gcs(self):
        """Descarga todos los archivos del modelo desde GCS."""
        logger.info("📥 Descargando archivos del modelo desde GCS...")

        client = storage.Client()
        bucket = client.bucket(self.bucket_name)

        blobs = list(bucket.list_blobs(prefix=f"{self.prefix}/"))

        if not blobs:
            raise FileNotFoundError(
                f"No se encontraron archivos bajo gs://{self.bucket_name}/{self.prefix}/"
            )

        self.model_path.mkdir(parents=True, exist_ok=True)

        for blob in blobs:
            filename = os.path.basename(blob.name)
            if not filename:  # evitar carpetas vacías
                continue

            dest = self.model_path / filename
            logger.info(f"⬇️  {filename}")
            blob.download_to_filename(dest)

        # Pausa leve para evitar race conditions en Cloud Run
        time.sleep(1)

        logger.info("✅ Descarga completada correctamente.")

    def load_model(self):
        """Carga el modelo HuggingFace desde disco."""
        if not self.model_path.exists() or not any(self.model_path.iterdir()):
            self._download_from_gcs()

        if self._pipeline is None:
            logger.info(f"⚙️ Cargando modelo desde: {self.model_path}")
            self._pipeline = pipeline("text-classification", model=str(self.model_path))
            logger.info("🎯 Modelo cargado correctamente en memoria.")

        return self._pipeline
