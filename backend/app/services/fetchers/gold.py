from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class GoldFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="gold", cache_ttl_seconds=1800)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "gold_24k_per_gram": 72.40,
            "gold_22k_per_gram": 66.35,
            "silver_per_gram": 0.88,
            "currency": "USD"
        }

    async def get_gold_prices(self) -> Dict[str, Any]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/gold",
            fallback_handler=self._fallback
        )
