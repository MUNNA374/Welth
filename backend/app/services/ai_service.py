from typing import Dict, Any, List
from backend.app.ai.gemini_client import GeminiClient
from backend.app.core.db import db

class AIService:
    def __init__(self):
        self.gemini = GeminiClient()

    async def get_financial_advice(self, user_id: str, query: str) -> Dict[str, Any]:
        # Gather user networth and budget context
        accounts = await db.account.find_many(where={"userId": user_id})
        balances_sum = sum(acc.balance for acc in accounts)
        context = f"User has {len(accounts)} accounts with total assets of {balances_sum} USD."
        
        response = await self.gemini.get_financial_advice(query, context)
        
        # Save to AI History log
        await db.aihistory.create(
            data={
                "userId": user_id,
                "prompt": query,
                "response": response.get("advice", ""),
                "type": "CHAT"
            }
        )
        return response

    async def get_monthly_ai_report(self, user_id: str) -> Dict[str, Any]:
        accounts = await db.account.find_many(where={"userId": user_id})
        balances_sum = sum(acc.balance for acc in accounts)
        
        cash_flow = {"inflow": 8500.0, "outflow": 6200.0, "net_cash_flow": 2300.0}
        budget_summary = "Entertainment spent 80%, Food spent 110% (exceeded)."
        
        report = await self.gemini.generate_monthly_report(cash_flow, budget_summary)
        
        # Save report database
        import json
        await db.report.create(
            data={
                "userId": user_id,
                "type": "MONTHLY",
                "title": f"AI Financial Report - June 2026",
                "contentJson": json.dumps(report)
            }
        )
        
        return report
