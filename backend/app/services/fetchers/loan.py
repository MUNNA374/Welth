from typing import Dict, Any
from backend.app.services.fetchers.base import BaseFetcher

class LoanEligibilityFetcher(BaseFetcher):
    def __init__(self):
        super().__init__(name="loan_eligibility", cache_ttl_seconds=3600)

    def _fallback(self) -> Dict[str, Any]:
        return {
            "eligible": True,
            "max_amount": 50000.0,
            "offered_rate": 7.5,
            "term_options_months": [12, 24, 36, 48]
        }

    async def check_loan_eligibility(self, user_id: str, loan_type: str, amount: float) -> Dict[str, Any]:
        return await self.fetch(
            url=f"https://api.mockfinance.com/v1/loans/eligibility?type={loan_type}&amount={amount}",
            fallback_handler=self._fallback
        )
