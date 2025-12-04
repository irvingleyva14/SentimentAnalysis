from fastapi import FastAPI
from app.api.routes.predict import router as predict_router
from app.services.model_loader import ModelLoader

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sentiment Analysis API",
        version="1.0.0"
    )

    # Cargar modelo 1 sola vez
    model_loader = ModelLoader()
    app.state.model = model_loader.load_model()

    # Aquí se registran los routers
    app.include_router(predict_router, prefix="/sentiment")

    return app

# Instancia para producción
app = create_app()
