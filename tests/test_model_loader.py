# tests/test_model_loader.py
import pytest

@pytest.mark.skip(reason="Requiere credenciales reales de GCS, saltar en CI")
def test_model_loader_initialization_local(monkeypatch):
    pass