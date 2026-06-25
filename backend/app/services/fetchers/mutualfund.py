from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class MutualFundFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="mutualfunds", cache_ttl_seconds=3600)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "NIFTY_50_INDEX": {"nav": 240.50, "growth": 1.2, "currency": "INR"},
            "S_AND_P_500_INDEX": {"nav": 520.10, "growth": 0.85, "currency": "USD"},
            "PARAG_PARIKH_FLEXI": {"nav": 74.20, "growth": 2.10, "currency": "INR"}
        }

    async def get_mutual_fund_navs(self) -> Dict[str, Any]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/mutualfunds",
            fallback_handler=self._fallback
        )
