from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.predict import router as predict_router
from app.services.model_loader import ModelLoader
from app.core.logger import setup_logger
import time
from app.config import settings

logger = setup_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


    # ----------------------------
    # CORS Middleware
    # ----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En PROD: poner dominios autorizados
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----------------------------
    # Load Model once
    # ----------------------------
    logger.info("📦 Cargando modelo en startup...")
    model_loader = ModelLoader(settings.MODEL_PATH)
    app.state.model = model_loader.load_model()
    logger.info("✔️ Modelo cargado en memoria")

    # ----------------------------
    # Healthcheck Endpoint
    # ----------------------------
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # ----------------------------
    # Global Exception Handler
    # ----------------------------
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Error en request: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"},
        )

    # ----------------------------
    # Logging Middleware
    # ----------------------------
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        process_time = (time.time() - start) * 1000

        logger.info(
            f"{request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.2f}ms"
        )
        return response

    app.include_router(predict_router, prefix="/sentiment")

    return app

app = create_app()
