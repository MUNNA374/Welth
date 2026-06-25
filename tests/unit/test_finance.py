from backend.app.finance.cashflow import calculate_cash_flow
from backend.app.finance.emi import calculate_emi
from backend.app.finance.health_score import calculate_financial_health_score
from backend.app.finance.tax import calculate_income_tax

def test_cashflow_calculation():
    txs = [
        {"amount": 1000.0, "type": "INFLOW"},
        {"amount": 250.0, "type": "OUTFLOW"},
        {"amount": 50.0, "type": "OUTFLOW"}
    ]
    res = calculate_cash_flow(txs)
    assert res["inflow"] == 1000.0
    assert res["outflow"] == 300.0
    assert res["net_cash_flow"] == 700.0

def test_emi_calculation():
    # $10,000 principal, 12% annual rate, 12 months term
    res = calculate_emi(10000.0, 12.0, 12)
    assert res["monthly_emi"] > 0
    assert res["total_amount_payable"] > 10000.0

def test_tax_calculation():
    # Gross income $50,000 US progresive tax
    res = calculate_income_tax(50000.0)
    assert res["gross_income"] == 50000.0
    assert res["total_tax"] > 0
    assert res["net_income"] < 50000.0

def test_financial_health_score():
    res = calculate_financial_health_score(
        monthly_income=5000.0,
        monthly_savings=1000.0,      # 20% savings rate (good)
        monthly_debt_payments=500.0,  # 10% DTI (good)
        emergency_fund_balance=15000.0,# 3 months of expenses (fair)
        monthly_expenses=3500.0,
        credit_score=760               # excellent
    )
    assert res["score"] >= 70
    assert res["rating"] in ["GOOD", "EXCELLENT"]
