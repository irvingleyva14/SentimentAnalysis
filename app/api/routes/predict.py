# app/api/routes/predict.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.predictor_service import PredictorService
from app.api.dependencies import get_predictor_service

#router = APIRouter(prefix="/predict", tags=["Prediction"])
router = APIRouter()

class InputText(BaseModel):
    text: str

@router.post("/")
async def predict_sentiment(
    payload: InputText,
    predictor_service: PredictorService = Depends(get_predictor_service)
):
    """Realiza una predicción de sentimiento desde JSON body."""
    
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    result = predictor_service.predict(text)

    output = result[0] if isinstance(result, list) else result

    return {
        "input_text": text,
        "label": output.get("label"),
        "score": float(output.get("score", 0))
    }
