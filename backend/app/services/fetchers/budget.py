from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class BudgetOptimizerFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="budget_optimizer", cache_ttl_seconds=1800)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "optimized_allocations": {
                "FOOD": 0.15,
                "RENT": 0.35,
                "UTILITIES": 0.10,
                "INVESTMENT": 0.20,
                "ENTERTAINMENT": 0.10,
                "SAVINGS": 0.10
            },
            "estimated_savings_increase": 12.5,
            "message": "Reduce Dining out by 5% and redirect funds to Stocks."
        }

    async def optimize_budget(self, user_id: str) -> Dict[str, Any]:
        return await self.fetch(
            url=f"https://api.mockfinance.com/v1/budget/optimize/{user_id}",
            fallback_handler=self._fallback
        )
