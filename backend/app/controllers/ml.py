from fastapi import APIRouter, Depends
from backend.app.api.deps import get_current_user
from backend.app.ml.pipeline import MLPipeline
from backend.app.repositories.transaction_repository import TransactionRepository
from typing import Any

router = APIRouter()
tx_repo = TransactionRepository()

@router.post("/train")
async def train_user_model(current_user: Any = Depends(get_current_user)):
    txs = await tx_repo.get_by_user(current_user.id, limit=300)
    tx_dicts = [{"amount": t.amount, "type": t.type, "date": t.date.isoformat()} for t in txs]
    
    pipeline = MLPipeline(current_user.id)
    processed_df = pipeline.preprocess_data(tx_dicts)
    results = pipeline.train_model(processed_df)
    return {"message": "Model training complete", "results": results}

@router.get("/forecast")
async def forecast_spending(current_user: Any = Depends(get_current_user)):
    # Grab last 3 days outflows
    from backend.app.core.db import db
    outflows = await db.transaction.find_many(
        where={"userId": current_user.id, "type": "OUTFLOW"},
        order={"date": "desc"},
        take=3
    )
    
    last_3 = [t.amount for t in outflows]
    # pad with average if fewer than 3
    while len(last_3) < 3:
        last_3.append(50.0)
        
    pipeline = MLPipeline(current_user.id)
    prediction = pipeline.predict_next_day(last_3)
    
    # Simple forecast analysis
    from backend.app.finance.forecast import forecast_next_period_spending
    analysis = forecast_next_period_spending(last_3)
    
    return {
        "predicted_next_day_spending": prediction,
        "trend_analysis": analysis
    }
