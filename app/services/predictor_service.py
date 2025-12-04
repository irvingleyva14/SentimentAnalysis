# app/services/predictor_service.py

from app.core.logger import setup_logger

logger = setup_logger(__name__)

class PredictorService:
    """Servicio encargado únicamente de realizar predicciones con el modelo pre-cargado."""

    def __init__(self, model):
        self.model = model
        self.logger = logger

    def predict(self, text: str):
        if not text.strip():
            raise ValueError("El texto de entrada no puede estar vacío.")
        
        self.logger.info(f"Realizando predicción sobre el texto: {text}")
        result = self.model(text)
        self.logger.info(f"Predicción completada: {result}")
        return result
