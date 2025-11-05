# app/api/dependencies.py
from app.services.predictor_service import PredictorService
from app.services.model_loader import ModelLoader

# Instancias únicas (singleton simple)
_model_loader_instance = None
_predictor_service_instance = None

def get_predictor_service() -> PredictorService:
    """Proporciona una instancia única de PredictorService para toda la app."""
    global _model_loader_instance, _predictor_service_instance

    if _model_loader_instance is None:
        _model_loader_instance = ModelLoader()  # Crea el cargador del modelo

    if _predictor_service_instance is None:
        _predictor_service_instance = PredictorService(_model_loader_instance)

    return _predictor_service_instance
