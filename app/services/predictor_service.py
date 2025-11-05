# app/services/predictor_service.py
from app.services.model_loader import ModelLoader
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class PredictorService:
    """Servicio encargado de generar predicciones usando el modelo cargado."""

    def __init__(self, model_loader: ModelLoader | None = None, model_path: str = "models/multilingual-sentiment"):
        """
        Si no se pasa un model_loader externo, crea uno con la ruta por defecto.
        Esto permite inyección de dependencias (útil para testing y mantenibilidad).
        """
        self.model_loader = model_loader or ModelLoader(model_path)
        self.model = None

    def initialize_model(self):
        """Carga el modelo solo una vez (si no está ya en memoria)."""
        if self.model is None:
            try:
                logger.info("Inicializando el modelo de predicción...")
                self.model = self.model_loader.load_model()
                logger.info("Modelo inicializado correctamente.")
            except Exception as e:
                logger.error(f"Error al inicializar el modelo: {e}")
                raise e

    def predict(self, text: str):
        """
        Realiza la predicción sobre un texto.
        Retorna el resultado del modelo en formato JSON.
        """
        if self.model is None:
            logger.warning("El modelo no estaba inicializado. Cargando...")
            self.initialize_model()

        try:
            logger.info(f"Realizando predicción sobre el texto: {text}")
            prediction = self.model(text)
            logger.info(f"Predicción completada: {prediction}")
            return prediction
        except Exception as e:
            logger.error(f"Error durante la predicción: {e}")
            raise e
