from fastapi import FastAPI
from app.api.routes.predict import router as predict_router

app = FastAPI(title="Sentiment Analysis API")

# Endpoint raíz
@app.get("/")
def root():
    return {"ok": True, "msg": "API viva"}

# Incluir el router con las rutas /predict y /batch_predict
app.include_router(predict_router)
