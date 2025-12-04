from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.predict import router as predict_router
from app.services.model_loader import ModelLoader
from app.core.logger import setup_logger
from app.config import settings
from uuid import uuid4
import time

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logger = setup_logger(__name__)

# Prometheus Metrics
SERVICE_NAME = "sentiment-api"

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "path"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["service", "method", "path"]
)


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
        allow_origins=["*"],
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
    # Metrics Endpoint
    # ----------------------------
    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    # ----------------------------
    # Logging + Metrics Middleware
    # ----------------------------
    @app.middleware("http")
    async def log_requests(request: Request, call_next):

        trace_id = str(uuid4())
        request.state.trace_id = trace_id

        method = request.method
        path = request.url.path

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # Prometheus metrics
        REQUEST_COUNT.labels(service=SERVICE_NAME, method=method, path=path).inc()
        REQUEST_LATENCY.labels(service=SERVICE_NAME, method=method, path=path).observe(duration)

        # JSON Logging
        logger.info(
            f"{method} {path} completed",
            extra={
                "trace_id": trace_id,
                "method": method,
                "path": path,
                "status": response.status_code,
                "latency_ms": round(duration * 1000, 2)
            }
        )

        response.headers["X-Trace-Id"] = trace_id
        return response

    # ----------------------------
    # Exception Handler
    # ----------------------------
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        trace_id = getattr(request.state, "trace_id", None)
        logger.error(str(exc), extra={"trace_id": trace_id})
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor", "trace_id": trace_id},
        )

    # ----------------------------
    # Healthcheck Endpoint
    # ----------------------------
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # ----------------------------
    # Routers
    # ----------------------------
    app.include_router(predict_router, prefix="/sentiment")

    return app


app = create_app()
