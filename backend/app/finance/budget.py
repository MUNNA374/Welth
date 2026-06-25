from typing import Dict, Any, List

def analyze_budget_status(budget_amount: float, spent_amount: float) -> Dict[str, Any]:
    """Compare budget limit with actual spending and generate alert flags."""
    remaining = budget_amount - spent_amount
    usage_pct = (spent_amount / budget_amount * 100) if budget_amount > 0 else 0
    
    status = "OK"
    if usage_pct >= 100:
        status = "EXCEEDED"
    elif usage_pct >= 85:
        status = "WARNING"
        
    return {
        "budget_limit": round(budget_amount, 2),
        "total_spent": round(spent_amount, 2),
        "remaining_amount": round(remaining, 2),
        "usage_percentage": round(usage_pct, 2),
        "status": status
    }
