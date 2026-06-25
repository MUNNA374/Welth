from fastapi import APIRouter, Depends, status
from backend.app.services.budget_service import BudgetService
from backend.app.api.deps import get_current_user
from pydantic import BaseModel
from typing import Optional, Any, List

router = APIRouter()
budget_service = BudgetService()

class BudgetCreate(BaseModel):
    category: str
    amount: float
    period: Optional[str] = "MONTHLY"
    startDate: str
    endDate: str

@router.get("/", response_model=List[Any])
async def get_budgets(current_user: Any = Depends(get_current_user)):
    budgets = await budget_service.list_budgets(current_user.id)
    return budgets

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_budget(budget_in: BudgetCreate, current_user: Any = Depends(get_current_user)):
    budget = await budget_service.create_budget(current_user.id, budget_in.model_dump())
    return budget

@router.get("/alerts")
async def check_alerts(current_user: Any = Depends(get_current_user)):
    alerts = await budget_service.check_user_budget_alerts(current_user.id)
    return {"alerts": alerts}
