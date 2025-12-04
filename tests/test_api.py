# tests/test_api.py
import pytest

# NO importes 'app' aquí globalmente. Usaremos la fixture 'client'.

@pytest.mark.unit
def test_predict_valid_text(client):
    # El endpoint espera un JSON body, no query params
    response = client.post("/sentiment/predict/", json={"text": "Buen día"})
    
    assert response.status_code == 200
    body = response.json()

    assert "label" in body
    assert "score" in body
    # Como está mockeado en conftest.py, siempre será POSITIVE
    assert body["label"] == "POSITIVE"

@pytest.mark.unit
def test_predict_missing_text_validation(client):
    # Enviar JSON vacío debería dar error de validación (422) o 400 según tu lógica
    response = client.post("/sentiment/predict/", json={})
    assert response.status_code == 422