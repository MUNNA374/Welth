from typing import List, Dict, Any

def calculate_net_worth(accounts: List[Dict[str, Any]], loans: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Net worth is calculated as Assets (accounts, investments) minus Liabilities (loans)."""
    assets = sum(acc.get("balance", 0.0) for acc in accounts)
    liabilities = sum(loan.get("outstandingBalance", 0.0) for loan in loans)
    
    return {
        "total_assets": round(assets, 2),
        "total_liabilities": round(liabilities, 2),
        "net_worth": round(assets - liabilities, 2)
    }
