from typing import List, Dict, Any, Optional
from backend.app.repositories.transaction_repository import TransactionRepository
from backend.app.ai.gemini_client import GeminiClient
from backend.app.finance.cashflow import calculate_cash_flow
from backend.app.core.db import db
from backend.app.notifications.in_app import create_in_app_notification
import datetime

class TransactionService:
    def __init__(self):
        self.tx_repo = TransactionRepository()
        self.ai_client = GeminiClient()

    async def list_transactions(self, user_id: str, limit: int = 100) -> List[Any]:
        return await self.tx_repo.get_by_user(user_id, limit=limit)

    async def create_transaction(self, user_id: str, tx_data: Dict[str, Any]) -> Any:
        # Check if category needs AI auto-categorization
        description = tx_data.get("description", "")
        category = tx_data.get("category")
        
        if not category or category.upper() == "OTHER":
            ai_res = await self.ai_client.categorize_transaction(description)
            tx_data["category"] = ai_res.get("category", "OTHER")
            if ai_res.get("merchant") != "UNKNOWN":
                tx_data["description"] = f"{ai_res.get('merchant')} - {description}"
        
        # Fraud check
        fraud_check = await self.ai_client.detect_fraud_anomalies(tx_data, "No recent high value flags")
        if fraud_check.get("is_fraud"):
            tx_data["isFraud"] = True
            await create_in_app_notification(
                user_id=user_id,
                title="Suspicious Transaction Alert",
                message=f"A transaction for {tx_data.get('amount')} under {tx_data.get('category')} looks suspicious.",
                notification_type="ALERT"
            )
            
        return await self.tx_repo.create({
            "userId": user_id,
            "accountId": tx_data["accountId"],
            "amount": float(tx_data["amount"]),
            "currency": tx_data.get("currency", "USD"),
            "category": tx_data["category"],
            "description": tx_data.get("description"),
            "type": tx_data["type"].upper(),
            "status": tx_data.get("status", "COMPLETED"),
            "isFraud": tx_data.get("isFraud", False),
            "source": tx_data.get("source", "MANUAL"),
            "date": datetime.datetime.fromisoformat(tx_data["date"]) if "date" in tx_data else datetime.datetime.now()
        })

    async def get_cashflow_analysis(self, user_id: str) -> Dict[str, Any]:
        txs = await self.tx_repo.get_by_user(user_id, limit=500)
        # Convert objects to serializable dicts
        tx_dicts = []
        for tx in txs:
            tx_dicts.append({
                "amount": tx.amount,
                "type": tx.type
            })
        return calculate_cash_flow(tx_dicts)
