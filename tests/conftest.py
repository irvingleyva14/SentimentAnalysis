# tests/conftest.py
import pytest
from unittest.mock import MagicMock
import os

# Evitar que cualquier librería intente buscar credenciales reales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/dummy_creds.json"

@pytest.fixture(scope="session", autouse=True)
def mock_model_loading():
    """
    Parche global: Reemplaza la carga del modelo real por un Mock.
    Esto evita que se conecte a GCS o descargue archivos pesados.
    """
    with pytest.MonkeyPatch.context() as m:
        # 1. Crear un 'pipeline' falso de Hugging Face
        mock_pipeline = MagicMock()
        # Cuando se llame al modelo, devolverá siempre POSITIVE
        mock_pipeline.return_value = [{"label": "POSITIVE", "score": 0.99}]
        
        # 2. Reemplazar el método 'load_model' de tu clase ModelLoader
        # para que devuelva el pipeline falso en lugar de cargar el real.
        m.setattr("app.services.model_loader.ModelLoader.load_model", lambda self: mock_pipeline)
        
        # 3. Reemplazar '_download_from_gcs' para asegurar que no toque la red
        m.setattr("app.services.model_loader.ModelLoader._download_from_gcs", lambda self: None)
        
        yield mock_pipeline

@pytest.fixture
def client(mock_model_loading):
    """
    Cliente de prueba que usa la app con el modelo ya mockeado.
    """
    from fastapi.testclient import TestClient
    from app.main import create_app
    
    # Importamos y creamos la app AQUI, dentro de la fixture,
    # cuando el mock ya está activo.
    app = create_app()
    return TestClient(app)