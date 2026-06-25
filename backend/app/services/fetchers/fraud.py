from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class FraudDetectionFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="fraud_detection", cache_ttl_seconds=10)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "is_fraud": False,
            "confidence_score": 0.02,
            "flagged_rules": []
        }

    async def check_fraud(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/fraud/check",
            fallback_handler=self._fallback
        )
