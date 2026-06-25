from typing import Dict, Any

def calculate_financial_health_score(
    monthly_income: float,
    monthly_savings: float,
    monthly_debt_payments: float,
    emergency_fund_balance: float,
    monthly_expenses: float,
    credit_score: int
) -> Dict[str, Any]:
    """Calculate a comprehensive health score from 0 to 100."""
    score = 0
    reasons = []

    # 1. Savings Rate (30 points) - target >= 20%
    savings_rate = (monthly_savings / monthly_income) if monthly_income > 0 else 0
    if savings_rate >= 0.20:
        score += 30
        reasons.append("+ Saving rate is healthy (20%+).")
    elif savings_rate >= 0.10:
        score += 15
        reasons.append("+ Saving rate is fair (10%-20%).")
    else:
        reasons.append("- Low saving rate (below 10%). Target at least 20%.")

    # 2. Debt to Income Ratio (20 points) - target <= 36%
    dti = (monthly_debt_payments / monthly_income) if monthly_income > 0 else 0
    if dti <= 0.36:
        score += 20
        reasons.append("+ Debt-to-income ratio is in control (under 36%).")
    elif dti <= 0.50:
        score += 10
        reasons.append("+ Debt-to-income ratio is moderate.")
    else:
        reasons.append("- High debt-to-income ratio (above 50%). Lower credit usage.")

    # 3. Emergency Fund Size (30 points) - target >= 3 to 6 months of expenses
    expense_multiplier = (emergency_fund_balance / monthly_expenses) if monthly_expenses > 0 else 0
    if expense_multiplier >= 6:
        score += 30
        reasons.append("+ Emergency fund is robust (6+ months of expenses).")
    elif expense_multiplier >= 3:
        score += 20
        reasons.append("+ Emergency fund is adequate (3-6 months).")
    else:
        reasons.append("- Emergency fund is small (under 3 months). Focus on liquidity.")

    # 4. Credit Score (20 points) - target >= 750
    if credit_score >= 750:
        score += 20
        reasons.append("+ Credit score is excellent (750+).")
    elif credit_score >= 650:
        score += 10
        reasons.append("+ Credit score is fair.")
    else:
        reasons.append("- Credit score is low (below 650). Make payments on time.")

    rating = "POOR"
    if score >= 80:
        rating = "EXCELLENT"
    elif score >= 60:
        rating = "GOOD"
    elif score >= 40:
        rating = "FAIR"

    return {
        "score": score,
        "rating": rating,
        "savings_rate_percent": round(savings_rate * 100, 2),
        "debt_to_income_percent": round(dti * 100, 2),
        "emergency_fund_months": round(expense_multiplier, 1),
        "reasons": reasons
    }
