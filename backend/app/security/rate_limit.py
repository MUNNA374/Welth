import logging
import time
from fastapi import HTTPException, Request, status
import redis
from backend.app.core.config import settings

logger = logging.getLogger("welth.rate_limit")

# Initialize Redis client (using connection pool)
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    # Ping to check if Redis is up
    redis_client.ping()
    redis_available = True
    logger.info("Rate limiter: Connected to Redis successfully.")
except Exception as e:
    redis_client = None
    redis_available = False
    logger.warning(f"Rate limiter: Redis not available. Falling back to open access. Error: {e}")

class RateLimiter:
    def __init__(self, requests_limit: int = 100, window_seconds: int = 60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds

    def __call__(self, request: Request):
        if not redis_available or not redis_client:
            return True

        # Identify client by IP (or user ID if authenticated)
        client_ip = request.client.host if request.client else "unknown"
        # We can also check if authorization token is in headers
        auth_header = request.headers.get("Authorization")
        identifier = f"rate_limit:{auth_header or client_ip}"

        try:
            current_time = int(time.time())
            # Use Redis transaction pipeline to get rolling window rate limiting
            pipe = redis_client.pipeline()
            # Remove timestamps older than the window
            pipe.zremrangebyscore(identifier, 0, current_time - self.window_seconds)
            # Add current timestamp
            pipe.zadd(identifier, {str(current_time): current_time})
            # Count elements in the window
            pipe.zcard(identifier)
            # Set TTL for the key
            pipe.expire(identifier, self.window_seconds)
            
            _, _, request_count, _ = pipe.execute()
            
            if request_count > self.requests_limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later."
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"RateLimiter check failed: {e}")
            # Fail-open
            return True
            
        return True
