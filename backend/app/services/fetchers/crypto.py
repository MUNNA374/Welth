from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class CryptoFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="crypto", cache_ttl_seconds=30)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "BTC": {"price": 67250.00, "change": 1.45, "currency": "USD"},
            "ETH": {"price": 3520.50, "change": 2.10, "currency": "USD"},
            "SOL": {"price": 142.80, "change": -0.75, "currency": "USD"},
            "ADA": {"price": 0.48, "change": 0.05, "currency": "USD"}
        }

    async def get_crypto_prices(self) -> Dict[str, Any]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/crypto",
            fallback_handler=self._fallback
        )
