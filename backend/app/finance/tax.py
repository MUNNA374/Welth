from typing import Dict, Any

def calculate_income_tax(income: float, country: str = "US") -> Dict[str, Any]:
    """A simple progressive tax rate simulator."""
    # Progressive brackets logic simulation (e.g. US Federal standard single 2024 simplified)
    tax = 0.0
    brackets = [
        (11600, 0.10),
        (47150, 0.12),
        (100525, 0.22),
        (191950, 0.24),
        (243725, 0.32),
        (609350, 0.35),
        (float('inf'), 0.37)
    ]
    
    prev_limit = 0.0
    remaining_income = income
    
    for limit, rate in brackets:
        bracket_size = limit - prev_limit
        if remaining_income > bracket_size:
            tax += bracket_size * rate
            remaining_income -= bracket_size
            prev_limit = limit
        else:
            tax += remaining_income * rate
            break
            
    effective_rate = (tax / income * 100) if income > 0 else 0
    return {
        "gross_income": round(income, 2),
        "total_tax": round(tax, 2),
        "net_income": round(income - tax, 2),
        "effective_tax_rate_percent": round(effective_rate, 2)
    }
