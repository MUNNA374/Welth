import logging
from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

logger = logging.getLogger("welth.fetchers.gold")

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
        """Fetch precious metal spot prices derived from GLD and SLV ETF prices."""
        try:
            url = "https://query1.finance.yahoo.com/v7/finance/quote"
            params = {"symbols": "GLD,SLV"}
            
            res = await self.fetch(url, params=params)
            result_list = res.get("quoteResponse", {}).get("result", [])
            
            prices = {}
            for item in result_list:
                sym = item.get("symbol")
                prices[sym] = float(item.get("regularMarketPrice", 0.0))
            
            gld_price = prices.get("GLD")
            slv_price = prices.get("SLV")
            
            if not gld_price or not slv_price:
                return self._fallback()
                
            # GLD represents approx 1/10th of an ounce of gold.
            # 1 troy ounce = 31.1035 grams.
            gold_per_gram_24k = (gld_price * 10) / 31.1035
            gold_per_gram_22k = gold_per_gram_24k * (22 / 24)
            # SLV represents approx 1 ounce of silver.
            silver_per_gram = slv_price / 31.1035
            
            return {
                "gold_24k_per_gram": round(gold_per_gram_24k, 2),
                "gold_22k_per_gram": round(gold_per_gram_22k, 2),
                "silver_per_gram": round(silver_per_gram, 2),
                "currency": "USD"
            }
        except Exception as e:
            logger.warning(f"Failed to fetch derived gold prices from Yahoo, using fallback: {e}")
            return self._fallback()
