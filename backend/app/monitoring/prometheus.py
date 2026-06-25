import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from backend.app.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Ignore metrics endpoints to avoid polluting stats
        if request.url.path == "/metrics" or request.url.path == "/api/v1/health":
            return await call_next(request)
            
        method = request.method
        endpoint = request.url.path
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
            return response
        except Exception as e:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="500").inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
            raise e

def get_metrics_response() -> Response:
    """Return current snapshot of Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
