import pytest
from app.services.model_loader import ModelLoader

def test_model_loader_initialization_local(monkeypatch):
    monkeypatch.setenv("MODEL_SOURCE", "local")
    loader = ModelLoader()
    model = loader.load_model()
    assert model is not None