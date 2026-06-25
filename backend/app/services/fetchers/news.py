from typing import List, Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class FinancialNewsFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="financial_news", cache_ttl_seconds=900)

    def _fallback(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": "Fed hints at interest rate cuts in coming quarters",
                "source": "Financial Times",
                "url": "https://ft.com/fed-rates",
                "summary": "The Federal Reserve suggests policy shifts as inflation metrics ease towards targets."
            },
            {
                "title": "Crypto markets rebound as institutional inflow increases",
                "source": "Bloomberg",
                "url": "https://bloomberg.com/crypto",
                "summary": "Bitcoin and Ether lead broad recoveries driven by ETF assets accumulation."
            }
        ]

    async def get_latest_news(self) -> List[Dict[str, Any]]:
        return await self.fetch(
            url="https://api.mockfinance.com/v1/news/financial",
            fallback_handler=self._fallback
        )
