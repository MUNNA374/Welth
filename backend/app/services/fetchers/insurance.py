from typing import Dict, Any, List
from backend.app.services.fetchers.base import BaseFetcher

class InsuranceQuoteFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="insurance_quotes", cache_ttl_seconds=3600)

    def _fallback(self) -> List[Dict[str, Any]]:
        return [
            {"provider": "Allianz", "premium_monthly": 45.0, "coverage_amount": 100000.0, "type": "LIFE"},
            {"provider": "Geico", "premium_monthly": 85.0, "coverage_amount": 50000.0, "type": "AUTO"},
            {"provider": "Aetna", "premium_monthly": 150.0, "coverage_amount": 500000.0, "type": "HEALTH"}
        ]

    async def get_quotes(self, user_details: Dict[str, Any]) -> List[Dict[str, Any]]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/insurance/quotes",
            fallback_handler=self._fallback
        )
