import pytest

# NO importamos 'app' aquí. Usamos el 'client' que ya tiene el modelo mockeado.

@pytest.mark.unit
def test_predict_valid_text(client):
    # Probamos el endpoint enviando un JSON válido
    response = client.post("/sentiment/predict/", json={"text": "Buen día"})
    
    # Validamos que responda 200 OK
    assert response.status_code == 200
    
    body = response.json()
    assert "label" in body
    assert "score" in body
    # El mock en conftest.py está configurado para devolver POSITIVE
    assert body["label"] == "POSITIVE"

@pytest.mark.unit
def test_predict_empty_text_validation(client):
    # Probamos que falle si enviamos texto vacío (Validación Pydantic/Lógica)
    response = client.post("/sentiment/predict/", json={"text": ""})
    
    # Debe ser 400 (según tu lógica en predict.py) o 422 (validación)
    assert response.status_code in [400, 422]