import shutil
import time
from typing import Dict, Any
from backend.app.core.db import db
from backend.app.security.rate_limit import redis_client, redis_available

async def check_system_health() -> Dict[str, Any]:
    """Execute health checks on various external dependencies and system state."""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {}
    }
    
    # 1. Database connection check
    try:
        db_connected = db.is_connected()
        health_status["services"]["database"] = {
            "status": "healthy" if db_connected else "unhealthy",
            "connected": db_connected
        }
        if not db_connected:
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"

    # 2. Redis check
    if redis_available and redis_client:
        try:
            redis_client.ping()
            health_status["services"]["redis"] = {
                "status": "healthy"
            }
        except Exception as e:
            health_status["services"]["redis"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"
    else:
        health_status["services"]["redis"] = {
            "status": "unavailable",
            "details": "Redis connection not configured or not running"
        }

    # 3. Disk Space check
    try:
        total, used, free = shutil.disk_usage("/")
        health_status["services"]["disk"] = {
            "status": "healthy" if (free / total) > 0.05 else "unhealthy",
            "free_percent": round((free / total) * 100, 2),
            "free_gb": round(free / (1024 ** 3), 2)
        }
    except Exception as e:
        health_status["services"]["disk"] = {
            "status": "unknown",
            "error": str(e)
        }

    return health_status
