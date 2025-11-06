# app/services/model_loader.py
from transformers import pipeline
from app.core.logger import setup_logger
from google.cloud import storage
import tarfile
from pathlib import Path
import os

logger = setup_logger(__name__)

class ModelLoader:
    """Se encarga de cargar el modelo desde local o, si no existe, desde GCS."""

    def __init__(
        self,
        model_path: str = "models/multilingual-sentiment",
        bucket_name: str = "model-senti-analy-ia",
        model_filename: str = "multilingual-sentiment.tar.gz"
    ):
        self.model_path = Path(model_path)
        self.bucket_name = bucket_name
        self.model_filename = model_filename
        self._pipeline = None

    def _download_from_gcs(self):
        """Descarga el archivo del modelo desde GCS y lo descomprime."""
        client = storage.Client()
        bucket = client.bucket(self.bucket_name)
        blob = bucket.blob(self.model_filename)

        local_tar = self.model_path.parent / self.model_filename
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

        if not local_tar.exists():
            logger.info(f"📦 Descargando {self.model_filename} desde GCS...")
            blob.download_to_filename(local_tar)
            logger.info("✅ Descarga completada.")

        if not self.model_path.exists():
            logger.info("🗜️  Descomprimiendo modelo...")
            with tarfile.open(local_tar, "r:gz") as tar:
                tar.extractall(self.model_path.parent)
            logger.info("✅ Descompresión completada.")

    def load_model(self):
        """Carga el modelo y lo mantiene en memoria."""
        if not self.model_path.exists():
            self._download_from_gcs()

        if self._pipeline is None:
            logger.info(f"⚙️ Cargando modelo desde: {self.model_path}")
            self._pipeline = pipeline("text-classification", model=str(self.model_path))
            logger.info("✅ Modelo cargado correctamente.")
        return self._pipeline
