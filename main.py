from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi import HTTPException
from typing import List


app = FastAPI(title="HF + FastAPI Demo")

# Carga del pipeline
nlp = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Endpoint raíz
@app.get("/")
def root():
    return {"ok": True, "msg": "API viva"}

# Esquema de entrada con Pydantic
class TextInput(BaseModel):
    text: str

# Endpoint de predicción
@app.post("/predict")
def predict(input: TextInput):
    if not input.text.strip():  # valida que el texto no esté vacío
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    result = nlp(input.text)[0]
    return {"text": input.text, "label": result["label"], "score": float(result["score"])}
"""
@app.post("/predict")
def predict(input: TextInput):
    result = nlp(input.text)[0]  # Tomamos solo el primer resultado
    return {"text": input.text, "label": result["label"], "score": float(result["score"])}
"""

class BatchInput(BaseModel):
    texts: List[str]

@app.post("/batch_predict")
def batch_predict(input: BatchInput):
    if not input.texts:
        raise HTTPException(status_code=400, detail="La lista de textos no puede estar vacía")
    results = [nlp(t)[0] for t in input.texts]
    return [{"text": t, "label": r["label"], "score": float(r["score"])} 
            for t, r in zip(input.texts, results)]
