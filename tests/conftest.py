import pytest
from unittest.mock import MagicMock
import os

# 1. Definimos credenciales falsas para engañar a Google Auth
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/dummy.json"

@pytest.fixture(scope="session", autouse=True)
def mock_model_loader():
    """Intercepta la carga del modelo para no usar GCS."""
    with pytest.MonkeyPatch.context() as m:
        mock_pipeline = MagicMock()
        mock_pipeline.return_value = [{"label": "POSITIVE", "score": 0.99}]
        
        # Parcheamos la clase ModelLoader donde sea que se use
        m.setattr("app.services.model_loader.ModelLoader.load_model", lambda self: mock_pipeline)
        m.setattr("app.services.model_loader.ModelLoader._download_from_gcs", lambda self: None)
        yield mock_pipeline

@pytest.fixture(scope="session")
def client(mock_model_loader):
    from fastapi.testclient import TestClient
    from app.main import create_app
    
    # Creamos la app AQUI, dentro de la fixture, protegidos por el mock
    app = create_app()
    with TestClient(app) as c:
        yield c