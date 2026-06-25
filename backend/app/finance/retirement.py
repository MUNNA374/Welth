from typing import Dict, Any

def plan_retirement(
    current_age: int,
    retirement_age: int,
    current_savings: float,
    monthly_contribution: float,
    annual_return: float,
    inflation_rate: float
) -> Dict[str, Any]:
    """Calculate compound interest savings at retirement adjusted for inflation."""
    years_to_grow = retirement_age - current_age
    if years_to_grow <= 0:
        return {"future_value": round(current_savings, 2), "inflation_adjusted_value": round(current_savings, 2)}
        
    # Real rate of return adjusted for inflation
    real_rate = ((1 + annual_return / 100) / (1 + inflation_rate / 100)) - 1
    monthly_rate = real_rate / 12
    months = years_to_grow * 12
    
    # Compound existing savings
    fv_existing = current_savings * ((1 + monthly_rate) ** months)
    
    # Future value of ordinary annuity for monthly contributions
    fv_contributions = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    
    total_fv = fv_existing + fv_contributions
    
    # Calculate nominal future value (without inflation adjustment for comparison)
    nominal_monthly_rate = (annual_return / 100) / 12
    fv_existing_nominal = current_savings * ((1 + nominal_monthly_rate) ** months)
    fv_contributions_nominal = monthly_contribution * (((1 + nominal_monthly_rate) ** months - 1) / nominal_monthly_rate) * (1 + nominal_monthly_rate)
    total_fv_nominal = fv_existing_nominal + fv_contributions_nominal
    
    return {
        "target_retirement_age": retirement_age,
        "years_to_retirement": years_to_grow,
        "nominal_future_value": round(total_fv_nominal, 2),
        "inflation_adjusted_future_value": round(total_fv, 2)
    }
