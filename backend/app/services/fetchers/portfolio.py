from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class PortfolioPerformanceFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="portfolio_performance", cache_ttl_seconds=300)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "total_value": 125000.0,
            "absolute_return": 15600.0,
            "return_percentage": 14.25,
            "allocation": {
                "STOCKS": 60,
                "MUTUAL_FUNDS": 25,
                "CRYPTO": 10,
                "GOLD": 5
            }
        }

    async def get_portfolio_performance(self, user_id: str) -> Dict[str, Any]:
        return await self.fetch(
            url=f"https://api.mockfinance.com/v1/portfolio/{user_id}/performance",
            fallback_handler=self._fallback
        )
