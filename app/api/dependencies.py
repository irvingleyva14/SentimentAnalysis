# app/api/dependencies.py

from fastapi import Request
from app.services.predictor_service import PredictorService

def get_model(request: Request):
    """Obtiene el modelo almacenado en el estado de la app."""
    return request.app.state.model

def get_predictor_service(request: Request):
    """Crea un servicio Predictor que usa el modelo ya cargado."""
    model = request.app.state.model
    return PredictorService(model)
