from fastapi import APIRouter, Depends
from backend.app.controllers import auth, user, transaction, budget, investment, ai, ml
from backend.app.security.rate_limit import RateLimiter

gateway_router = APIRouter()

# Define global gateway rate limiting (e.g., 100 requests per minute)
global_rate_limiter = RateLimiter(requests_limit=120, window_seconds=60)

# Register controllers under the gateway router with appropriate tags and dependencies
gateway_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentication"]
)
gateway_router.include_router(
    user.router, 
    prefix="/users", 
    tags=["User Management"], 
    dependencies=[Depends(global_rate_limiter)]
)
gateway_router.include_router(
    transaction.router, 
    prefix="/transactions", 
    tags=["Transactions"], 
    dependencies=[Depends(global_rate_limiter)]
)
gateway_router.include_router(
    budget.router, 
    prefix="/budgets", 
    tags=["Budgets"], 
    dependencies=[Depends(global_rate_limiter)]
)
gateway_router.include_router(
    investment.router, 
    prefix="/investments", 
    tags=["Investments"], 
    dependencies=[Depends(global_rate_limiter)]
)
gateway_router.include_router(
    ai.router, 
    prefix="/ai", 
    tags=["AI Services"], 
    dependencies=[Depends(global_rate_limiter)]
)
gateway_router.include_router(
    ml.router, 
    prefix="/ml", 
    tags=["ML Predictions"], 
    dependencies=[Depends(global_rate_limiter)]
)
