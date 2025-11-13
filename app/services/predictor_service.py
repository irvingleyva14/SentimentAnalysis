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
        self.logger = logger  # Asigna el logger como atributo de instancia

    def _ensure_model_loaded(self):
        """Verifica que el modelo esté cargado antes de usarlo."""
        if self.model is None:
            self.logger.warning("El modelo no estaba inicializado. Cargando...")
            self.initialize_model()

    def initialize_model(self):
        """Carga el modelo solo una vez (si no está ya en memoria)."""
        if self.model is None:
            try:
                self.logger.info("Inicializando el modelo de predicción...")
                self.model = self.model_loader.load_model()
                self.logger.info("Modelo inicializado correctamente.")
            except Exception as e:
                self.logger.error(f"Error al inicializar el modelo: {e}")
                raise e

    def predict(self, text: str):
        """Realiza una predicción sobre el texto dado."""
        if not text.strip():
            raise ValueError("El texto de entrada no puede estar vacío.")
        
        self._ensure_model_loaded()
        self.logger.info(f"Realizando predicción sobre el texto: {text}")
        result = self.model(text)
        self.logger.info(f"Predicción completada: {result}")
        return result
