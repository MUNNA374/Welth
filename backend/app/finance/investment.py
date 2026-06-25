from typing import Dict, Any

def calculate_sip_future_value(monthly_investment: float, annual_rate: float, years: int) -> Dict[str, Any]:
    """SIP / Mutual Fund periodic investment future value: P * [ (1+i)^n - 1 ] * (1+i) / i"""
    monthly_rate = (annual_rate / 100) / 12
    months = years * 12
    
    if monthly_rate == 0:
        fv = monthly_investment * months
        invested = fv
        interest = 0.0
    else:
        fv = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        invested = monthly_investment * months
        interest = fv - invested
        
    return {
        "total_invested": round(invested, 2),
        "wealth_gain": round(interest, 2),
        "future_value": round(fv, 2)
    }
