import logging
from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

logger = logging.getLogger("welth.fetchers.crypto")

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
        """Fetch current crypto prices from CoinGecko simple price API."""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "bitcoin,ethereum,solana,cardano",
                "vs_currencies": "usd",
                "include_24hr_change": "true"
            }
            res = await self.fetch(url, params=params)
            
            return {
                "BTC": {
                    "price": float(res.get("bitcoin", {}).get("usd", 67250.00)),
                    "change": float(res.get("bitcoin", {}).get("usd_24h_change", 0.0)),
                    "currency": "USD"
                },
                "ETH": {
                    "price": float(res.get("ethereum", {}).get("usd", 3520.50)),
                    "change": float(res.get("ethereum", {}).get("usd_24h_change", 0.0)),
                    "currency": "USD"
                },
                "SOL": {
                    "price": float(res.get("solana", {}).get("usd", 142.80)),
                    "change": float(res.get("solana", {}).get("usd_24h_change", 0.0)),
                    "currency": "USD"
                },
                "ADA": {
                    "price": float(res.get("cardano", {}).get("usd", 0.48)),
                    "change": float(res.get("cardano", {}).get("usd_24h_change", 0.0)),
                    "currency": "USD"
                }
            }
        except Exception as e:
            logger.warning(f"CoinGecko API fetch failed, using fallback: {e}")
            return self._fallback()
