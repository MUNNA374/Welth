from typing import List, Dict, Any
from backend.app.repositories.budget_repository import BudgetRepository
from backend.app.finance.budget import analyze_budget_status
from backend.app.core.db import db
from backend.app.notifications.in_app import create_in_app_notification
import datetime

class BudgetService:
    def __init__(self):
        self.budget_repo = BudgetRepository()

    async def list_budgets(self, user_id: str) -> List[Any]:
        return await self.budget_repo.get_user_budgets(user_id)

    async def create_budget(self, user_id: str, budget_data: Dict[str, Any]) -> Any:
        return await self.budget_repo.create({
            "userId": user_id,
            "category": budget_data["category"].upper(),
            "amount": float(budget_data["amount"]),
            "period": budget_data.get("period", "MONTHLY").upper(),
            "startDate": datetime.datetime.fromisoformat(budget_data["startDate"]),
            "endDate": datetime.datetime.fromisoformat(budget_data["endDate"])
        })

    async def check_user_budget_alerts(self, user_id: str) -> List[Dict[str, Any]]:
        budgets = await self.list_budgets(user_id)
        alerts = []
        
        for b in budgets:
            # Query sum of outflows for this category during the budget period
            tx_sum = await db.transaction.aggregate(
                where={
                    "userId": user_id,
                    "category": b.category,
                    "type": "OUTFLOW",
                    "date": {
                        "gte": b.startDate,
                        "lte": b.endDate
                    }
                },
                sum={"amount": True}
            )
            spent = tx_sum.sum.amount or 0.0
            analysis = analyze_budget_status(b.amount, spent)
            
            if analysis["status"] in ["EXCEEDED", "WARNING"]:
                alerts.append({
                    "category": b.category,
                    "limit": b.amount,
                    "spent": spent,
                    "status": analysis["status"]
                })
                # Trigger In-App notification
                await create_in_app_notification(
                    user_id=user_id,
                    title=f"Budget {analysis['status'].lower()}",
                    message=f"You have spent {spent:.2f} of your {b.amount:.2f} budget for {b.category}.",
                    notification_type="ALERT"
                )
                
        return alerts
