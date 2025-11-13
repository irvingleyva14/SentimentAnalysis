from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_valid_text():
    response = client.post("/predict?text=Buen día")
    assert response.status_code == 200
    body = response.json()

    assert "label" in body
    assert "score" in body
    assert body["label"] in ["Positive", "Negative", "Neutral"]


def test_predict_missing_text():
    response = client.post("/predict")
    assert response.status_code == 422
