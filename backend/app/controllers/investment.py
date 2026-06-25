from fastapi import APIRouter, Depends
from backend.app.api.deps import get_current_user
from backend.app.services.fetchers.stocks import StockFetcher
from backend.app.services.fetchers.crypto import CryptoFetcher
from backend.app.services.fetchers.exchange import ExchangeRateFetcher
from backend.app.services.fetchers.news import FinancialNewsFetcher
from backend.app.core.db import db
from typing import Any

router = APIRouter()

@router.get("/")
async def get_investments(current_user: Any = Depends(get_current_user)):
    # Find accounts of type investment
    accounts = await db.account.find_many(where={"userId": current_user.id, "type": "INVESTMENT"})
    # Find all investments linked to these accounts
    account_ids = [acc.id for acc in accounts]
    investments = await db.investment.find_many(where={"accountId": {"in": account_ids}})
    return investments

@router.get("/market-data")
async def get_market_prices(current_user: Any = Depends(get_current_user)):
    stocks = await StockFetcher().get_stock_prices()
    crypto = await CryptoFetcher().get_crypto_prices()
    exchange = await ExchangeRateFetcher().get_exchange_rates()
    return {
        "stocks": stocks,
        "crypto": crypto,
        "exchange_rates": exchange
    }

@router.get("/news")
async def get_market_news(current_user: Any = Depends(get_current_user)):
    news = await FinancialNewsFetcher().get_latest_news()
    return {"news": news}
