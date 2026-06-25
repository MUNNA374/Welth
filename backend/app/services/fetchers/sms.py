from typing import Dict, Any, List
from backend.app.services.fetchers.base import BaseFetcher

class SMSTransactionParserFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="sms_parser", cache_ttl_seconds=10)

    def _fallback(self) -> List[Dict[str, Any]]:
        return [
            {
                "merchant": "Starbucks Coffee",
                "amount": 6.80,
                "date": "2026-06-25",
                "category": "FOOD",
                "sms_body": "Sent $6.80 to Starbucks on card ending 4242"
            }
        ]

    async def parse_sms(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.fetch(
            url=f"https://api.mockfinance.com/v1/parser/sms/{user_id}",
            fallback_handler=self._fallback
        )
