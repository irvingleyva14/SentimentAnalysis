# app/services/model_loader.py
from transformers import pipeline
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class ModelLoader:
    """Se encarga de cargar el modelo de Hugging Face desde local o GCS."""

    def __init__(self, model_path: str = "models/multilingual-sentiment"):
        self.model_path = model_path
        self._pipeline = None

    def load_model(self):
        """Carga el modelo y lo mantiene en memoria."""
        if self._pipeline is None:
            logger.info(f"Cargando modelo desde: {self.model_path}")
            self._pipeline = pipeline("text-classification", model=self.model_path)
            logger.info("✅ Modelo cargado correctamente.")
        return self._pipeline
