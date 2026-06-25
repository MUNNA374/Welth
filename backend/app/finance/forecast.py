from typing import List, Dict, Any

def forecast_next_period_spending(past_spending: List[float]) -> Dict[str, Any]:
    """Generates moving average based forecast for upcoming period."""
    if not past_spending:
        return {"forecasted_amount": 0.0, "confidence": "LOW"}
        
    # Calculate simple moving average
    sma = sum(past_spending) / len(past_spending)
    
    # Calculate simple trend direction (last vs first)
    trend = "STABLE"
    if len(past_spending) >= 2:
        if past_spending[-1] > past_spending[0]:
            trend = "INCREASING"
        elif past_spending[-1] < past_spending[0]:
            trend = "DECREASING"
            
    return {
        "forecasted_amount": round(sma, 2),
        "historical_average": round(sma, 2),
        "trend_direction": trend,
        "confidence": "MEDIUM" if len(past_spending) >= 3 else "LOW"
    }
