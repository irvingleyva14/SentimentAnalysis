from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import List
from functools import lru_cache
import os
import uvicorn

app = FastAPI(title="HF + FastAPI Demo")

# Carga diferida del modelo (lazy loading)
@lru_cache(maxsize=1)
def get_model():
    return pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

@app.get("/")
def root():
    return {"ok": True, "msg": "API viva"}

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input: TextInput):
        if not input.text.strip():  # valida que el texto no esté vacío
            raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
        nlp = get_model()
        result = nlp(input.text)[0]
        return {"text": input.text, "label": result["label"], "score": float(result["score"])}

class BatchInput(BaseModel):
    texts: List[str]

@app.post("/batch_predict")
def batch_predict(input: BatchInput):
    if not input.texts:
        raise HTTPException(status_code=400, detail="La lista de textos no puede estar vacía")
    nlp = get_model()
    results = [nlp(t)[0] for t in input.texts]
    return [{"text": t, "label": r["label"], "score": float(r["score"])} 
            for t, r in zip(input.texts, results)]

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Usa el puerto que Cloud Run define
    uvicorn.run(app, host="0.0.0.0", port=port)
