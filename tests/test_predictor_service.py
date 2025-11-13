import pytest
from app.services.predictor_service import PredictorService

@pytest.fixture
def predictor():
    return PredictorService()

def test_predictor_returns_valid_response(predictor):
    text = "Me encanta este proyecto"
    result = predictor.predict(text)
    assert "label" in result[0]
    assert "score" in result[0]
    assert isinstance(result[0]["score"], float)

def test_predictor_handles_empty_input(predictor):
    with pytest.raises(ValueError):
        predictor.predict("")
