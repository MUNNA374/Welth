import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.db import init_db, close_db
from backend.app.gateway import gateway_router
from backend.app.monitoring.prometheus import PrometheusMiddleware, get_metrics_response
from backend.app.monitoring.health import check_system_health
from backend.app.monitoring.sentry import init_sentry
from backend.app.monitoring.logging import setup_logging
from backend.app.security.csrf import verify_csrf_token

# Initialize logging and Sentry monitoring
setup_logging()
init_sentry()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database startup connection
    await init_db()
    yield
    # Database shutdown disconnection
    await close_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply Prometheus performance monitoring middleware
app.add_middleware(PrometheusMiddleware)

# Mount static uploads directory for handling receipts and assets locally
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Metrics Endpoint
@app.get("/metrics")
def metrics():
    """Exposes raw metrics for Prometheus scrapers."""
    return get_metrics_response()

# Health Check Endpoint
@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    """Endpoint returning status of DB, Cache, and disk usage."""
    status_payload = await check_system_health()
    status_code = 200 if status_payload["status"] in ["healthy", "degraded"] else 503
    return JSONResponse(content=status_payload, status_code=status_code)

# Include core Gateway Router
# Automatically apply CSRF token checks to all gateway mutation routes
app.include_router(
    gateway_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(verify_csrf_token)]
)
