from fastapi import APIRouter, Depends
from backend.app.services.ai_service import AIService
from backend.app.api.deps import get_current_user
from pydantic import BaseModel
from typing import Any

router = APIRouter()
ai_service = AIService()

class AdviceQuery(BaseModel):
    query: str

@router.post("/chat")
async def chat_advisor(body: AdviceQuery, current_user: Any = Depends(get_current_user)):
    advice = await ai_service.get_financial_advice(current_user.id, body.query)
    return advice

@router.post("/monthly-report")
async def run_monthly_report(current_user: Any = Depends(get_current_user)):
    report = await ai_service.get_monthly_ai_report(current_user.id)
    return report

@router.get("/recommendations")
async def get_investment_recommendations(current_user: Any = Depends(get_current_user)):
    from backend.app.ai.gemini_client import GeminiClient
    ai = GeminiClient()
    # Mocking user profile stats
    recommendations = await ai.recommend_investments(
        risk_profile="MODERATE",
        age=30,
        net_worth=45000.0
    )
    return recommendations
