from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class ReceiptOCRFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="receipt_ocr", cache_ttl_seconds=10)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "merchant": "Whole Foods Market",
            "amount": 84.50,
            "date": "2026-06-25",
            "category": "FOOD",
            "confidence": 0.94
        }

    async def process_receipt(self, file_url: str) -> Dict[str, Any]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/ocr/process",
            fallback_handler=self._fallback
        )
