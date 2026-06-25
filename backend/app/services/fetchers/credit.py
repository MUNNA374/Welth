from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class CreditScoreFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="credit_score", cache_ttl_seconds=86400)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "score": 750,
            "rating": "Excellent",
            "provider": "Experian",
            "last_updated": "2026-06-01"
        }

    async def fetch_credit_score(self, ssn_hash: str) -> Dict[str, Any]:
        return await self.fetch(
            url=f"https://api.mockfinance.com/v1/credit/{ssn_hash}",
            fallback_handler=self._fallback
        )
