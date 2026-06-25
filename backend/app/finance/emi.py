from typing import Dict, Any

def calculate_emi(principal: float, annual_rate: float, term_months: int) -> Dict[str, Any]:
    """Compute monthly EMI using Standard formula: P * r * (1+r)^n / ((1+r)^n - 1)"""
    if annual_rate == 0:
        emi = principal / term_months
        total_payable = principal
        total_interest = 0.0
    else:
        # Monthly interest rate
        r = (annual_rate / 100) / 12
        n = term_months
        emi = principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        total_payable = emi * n
        total_interest = total_payable - principal
        
    return {
        "monthly_emi": round(emi, 2),
        "principal_amount": round(principal, 2),
        "total_interest_payable": round(total_interest, 2),
        "total_amount_payable": round(total_payable, 2)
    }
