from typing import Dict, Any, List
from backend.app.services.fetchers.base import BaseFetcher

class EmailTransactionParserFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="email_parser", cache_ttl_seconds=10)

    def _fallback(self) -> List[Dict[str, Any]]:
        return [
            {
                "merchant": "Netflix",
                "amount": 15.49,
                "date": "2026-06-24",
                "category": "ENTERTAINMENT",
                "email_subject": "Your Netflix Invoice"
            }
        ]

    async def parse_emails(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.fetch(
            url=f"https://api.mockfinance.com/v1/parser/email/{user_id}",
            fallback_handler=self._fallback
        )
