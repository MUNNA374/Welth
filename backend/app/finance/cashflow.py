from typing import List, Dict, Any

def calculate_cash_flow(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute inflows, outflows, and net cash flow from a list of transactions."""
    inflow = 0.0
    outflow = 0.0
    for tx in transactions:
        amount = tx.get("amount", 0.0)
        tx_type = tx.get("type", "OUTFLOW").upper()
        if tx_type == "INFLOW":
            inflow += amount
        else:
            outflow += amount
            
    return {
        "inflow": round(inflow, 2),
        "outflow": round(outflow, 2),
        "net_cash_flow": round(inflow - outflow, 2)
    }
