import logging
from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

logger = logging.getLogger("welth.fetchers.stocks")

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
        """Fetch current stock prices from Yahoo Finance API with fallback."""
        try:
            url = "https://query1.finance.yahoo.com/v7/finance/quote"
            params = {"symbols": "AAPL,MSFT,GOOGL,TSLA,VOO"}
            
            res = await self.fetch(url, params=params)
            result_list = res.get("quoteResponse", {}).get("result", [])
            
            mapped = {}
            for item in result_list:
                sym = item.get("symbol")
                mapped[sym] = {
                    "price": float(item.get("regularMarketPrice", 0.0)),
                    "change": float(item.get("regularMarketChangePercent", 0.0)),
                    "currency": item.get("currency", "USD")
                }
            
            if all(k in mapped for k in ["AAPL", "MSFT", "GOOGL", "TSLA"]):
                return mapped
            return self._fallback()
        except Exception as e:
            logger.warning(f"Yahoo Finance Quote API fetch failed, using fallback: {e}")
            return self._fallback()
