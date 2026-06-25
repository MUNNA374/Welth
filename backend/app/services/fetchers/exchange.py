from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class ExchangeRateFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="exchange_rates", cache_ttl_seconds=3600)  # cache 1 hour

    def _fallback(self) -> Dict[str, Any]:
        return {
            "base": "USD",
            "rates": {
                "EUR": 0.92,
                "GBP": 0.79,
                "INR": 83.50,
                "JPY": 156.40,
                "CAD": 1.36,
                "AUD": 1.50
            }
        }

    async def get_exchange_rates(self) -> Dict[str, Any]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/exchange",
            fallback_handler=self._fallback
        )
