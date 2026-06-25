from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class StockFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="stocks", cache_ttl_seconds=60)

    def _fallback(self) -> Dict[str, Any]:
        """Return fallback mock stock data."""
        return {
            "AAPL": {"price": 182.52, "change": 1.25, "currency": "USD"},
            "MSFT": {"price": 420.55, "change": -0.80, "currency": "USD"},
            "GOOGL": {"price": 175.30, "change": 2.10, "currency": "USD"},
            "TSLA": {"price": 178.20, "change": -3.40, "currency": "USD"}
        }

    async def get_stock_prices(self) -> Dict[str, Any]:
        """Fetch current stock prices."""
        # Using a mock API endpoint, with fallback fallback handler
        return await self.fetch(
            url="https://api.mockfinance.com/v1/stocks",
            fallback_handler=self._fallback
        )
