import logging
from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

logger = logging.getLogger("welth.fetchers.exchange")

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
        """Fetch current currency exchange rates from Open ER API."""
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            res = await self.fetch(url)
            if res.get("result") == "success":
                rates = res.get("rates", {})
                return {
                    "base": "USD",
                    "rates": {
                        "EUR": float(rates.get("EUR", 0.92)),
                        "GBP": float(rates.get("GBP", 0.79)),
                        "INR": float(rates.get("INR", 83.50)),
                        "JPY": float(rates.get("JPY", 156.40)),
                        "CAD": float(rates.get("CAD", 1.36)),
                        "AUD": float(rates.get("AUD", 1.50))
                    }
                }
            return self._fallback()
        except Exception as e:
            logger.warning(f"Failed to fetch exchange rates from Open ER, using fallback: {e}")
            return self._fallback()
