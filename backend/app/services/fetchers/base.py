import time
import logging
import asyncio
from typing import Any, Callable, Optional, Dict
import httpx
from pydantic import BaseModel
from backend.app.security.rate_limit import redis_client, redis_available

logger = logging.getLogger("welth.fetchers.base")

class BaseFetcher:
    def __init__(
        self,
        name: str,
        cache_ttl_seconds: int = 300,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        backoff_factor: float = 2.0
    ):
        self.name = name
        self.cache_ttl = cache_ttl_seconds
        self.timeout = timeout_seconds
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    async def fetch(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        validation_model: Optional[type[BaseModel]] = None,
        fallback_handler: Optional[Callable[[], Any]] = None
    ) -> Any:
        """Fetch data from URL with caching, retries, timeout, and fallback."""
        
        # 1. Caching - Check Redis
        cache_key = f"fetcher:{self.name}:{url}:{hash(frozenset(params.items())) if params else ''}"
        if redis_available and redis_client:
            try:
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    logger.debug(f"Fetcher '{self.name}': Cache hit for {url}")
                    return cached_data
            except Exception as e:
                logger.warning(f"Fetcher '{self.name}' cache check failed: {e}")

        # 2. HTTP Request with Retries and Timeout
        retries = 0
        current_delay = 1.0
        last_error = None
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            while retries < self.max_retries:
                try:
                    logger.info(f"Fetcher '{self.name}': Fetching {url} (Attempt {retries+1}/{self.max_retries})")
                    response = await client.get(url, params=params, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    
                    # 3. Validation
                    if validation_model:
                        try:
                            # Validate using Pydantic model
                            validated = validation_model.model_validate(data)
                            data = validated.model_dump()
                        except Exception as val_err:
                            logger.error(f"Fetcher '{self.name}' response validation error: {val_err}")
                            raise ValueError(f"Response validation failed: {val_err}")

                    # 4. Cache the result in Redis
                    if redis_available and redis_client:
                        try:
                            redis_client.setex(cache_key, self.cache_ttl, str(data))
                        except Exception as cache_err:
                            logger.warning(f"Fetcher '{self.name}' saving to cache failed: {cache_err}")
                            
                    return data
                    
                except (httpx.HTTPError, ValueError) as err:
                    last_error = err
                    retries += 1
                    logger.warning(f"Fetcher '{self.name}' failed attempt {retries}: {err}")
                    if retries < self.max_retries:
                        await asyncio.sleep(current_delay)
                        current_delay *= self.backoff_factor

        # 5. Fallback - triggers on final failure
        logger.error(f"Fetcher '{self.name}' completely failed: {last_error}")
        if fallback_handler:
            logger.info(f"Fetcher '{self.name}': Executing fallback handler.")
            return fallback_handler()
            
        raise last_error
