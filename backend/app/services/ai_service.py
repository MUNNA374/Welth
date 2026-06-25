from typing import Dict, Any, List
from backend.app.ai.gemini_client import GeminiClient
from backend.app.core.db import db

class AIService:
    def __init__(self):
        self.gemini = GeminiClient()

    async def get_financial_advice(self, user_id: str, query: str) -> Dict[str, Any]:
        # 1. Gather Accounts
        accounts = await db.account.find_many(where={"userId": user_id})
        balances_sum = sum(acc.balance for acc in accounts)
        accounts_text = "\n".join([f"- {acc.name} ({acc.type}): ${acc.balance:,.2f}" for acc in accounts])

        # 2. Gather active Budgets
        budgets = await db.budget.find_many(where={"userId": user_id})
        budgets_text = "\n".join([f"- {b.category}: Limit ${b.amount:,.2f}" for b in budgets])

        # 3. Gather active Goals
        goals = await db.goal.find_many(where={"userId": user_id})
        goals_text = "\n".join([f"- {g.name}: Target ${g.targetAmount:,.2f}, Saved ${g.currentAmount:,.2f} ({g.status})" for g in goals])

        # 4. Gather recent transactions
        transactions = await db.transaction.find_many(
            where={"userId": user_id},
            order={"date": "desc"},
            take=15
        )
        tx_text = "\n".join([
            f"- {tx.date.date() if tx.date else 'Unknown Date'}: {tx.description} | {tx.category} | {'+' if tx.type == 'INFLOW' else '-'}${tx.amount:,.2f}"
            for tx in transactions
        ])

        # Combine into rich profile context
        context = f"""
=== USER FINANCIAL PROFILE ===
Total Assets Net Worth: ${balances_sum:,.2f}

ACCOUNTS:
{accounts_text if accounts_text else 'No active accounts.'}

ACTIVE BUDGETS:
{budgets_text if budgets_text else 'No active budgets defined.'}

SAVINGS GOALS:
{goals_text if goals_text else 'No active savings goals.'}

RECENT TRANSACTION HISTORY (Last 15):
{tx_text if tx_text else 'No recent transactions.'}
"""
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
