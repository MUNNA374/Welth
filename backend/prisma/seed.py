import asyncio
import logging
import datetime
import random
from backend.app.core.db import db, init_db, close_db
from backend.app.security.jwt import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("welth.seed")

async def seed_data():
    logger.info("Starting database seeding...")
    await init_db()
    
    # 1. Clean existing database
    try:
        await db.auditlog.delete_many()
        await db.aihistory.delete_many()
        await db.notification.delete_many()
        await db.report.delete_many()
        await db.receipt.delete_many()
        await db.subscription.delete_many()
        await db.bill.delete_many()
        await db.insurance.delete_many()
        await db.loan.delete_many()
        await db.investment.delete_many()
        await db.savings.delete_many()
        await db.goal.delete_many()
        await db.budget.delete_many()
        await db.transaction.delete_many()
        await db.account.delete_many()
        await db.settings.delete_many()
        await db.session.delete_many()
        await db.user.delete_many()
        logger.info("Cleaned up existing database records.")
    except Exception as e:
        logger.warning(f"Error while cleaning up database: {e}")

    # 2. Create Users
    admin_pw = get_password_hash("AdminPassword123")
    user_pw = get_password_hash("UserPassword123")
    
    admin = await db.user.create(
        data={
            "email": "admin@welth.com",
            "passwordHash": admin_pw,
            "firstName": "System",
            "lastName": "Admin",
            "role": "ADMIN"
        }
    )
    
    user = await db.user.create(
        data={
            "email": "user@welth.com",
            "passwordHash": user_pw,
            "firstName": "Alex",
            "lastName": "Finance",
            "role": "USER"
        }
    )
    
    logger.info("Users seeded successfully.")

    # Create Settings
    await db.settings.create(data={"userId": admin.id, "theme": "DARK", "currency": "USD"})
    await db.settings.create(data={"userId": user.id, "theme": "DARK", "currency": "USD"})

    # 3. Create 10 Accounts
    accounts_data = [
        {"name": "Chase Checking", "type": "BANK", "balance": 8420.50, "institution": "Chase Bank"},
        {"name": "Ally HY Savings", "type": "BANK", "balance": 35000.00, "institution": "Ally Bank"},
        {"name": "Fidelity Brokerage", "type": "INVESTMENT", "balance": 48200.00, "institution": "Fidelity"},
        {"name": "Vanguard 401(k)", "type": "INVESTMENT", "balance": 120000.00, "institution": "Vanguard"},
        {"name": "Coinbase Wallet", "type": "INVESTMENT", "balance": 12500.00, "institution": "Coinbase"},
        {"name": "Apple Card", "type": "CREDIT", "balance": -1450.00, "institution": "Goldman Sachs"},
        {"name": "Chase Sapphire Card", "type": "CREDIT", "balance": -2800.00, "institution": "Chase Bank"},
        {"name": "Physical Cash Wallet", "type": "CASH", "balance": 450.00, "institution": "Cash"},
        {"name": "Tesla Auto Loan", "type": "BANK", "balance": -18500.00, "institution": "Tesla Finance"},
        {"name": "Chase Home Mortgage", "type": "BANK", "balance": -320000.00, "institution": "Chase Bank"},
    ]

    accounts = []
    for acc in accounts_data:
        account_record = await db.account.create(
            data={
                "userId": user.id,
                "name": acc["name"],
                "type": acc["type"],
                "balance": acc["balance"],
                "currency": "USD",
                "institution": acc["institution"]
            }
        )
        accounts.append(account_record)

    checking_acc = next(a for a in accounts if a.name == "Chase Checking")
    savings_acc = next(a for a in accounts if a.name == "Ally HY Savings")
    brokerage_acc = next(a for a in accounts if a.name == "Fidelity Brokerage")
    retirement_acc = next(a for a in accounts if a.name == "Vanguard 401(k)")
    coinbase_acc = next(a for a in accounts if a.name == "Coinbase Wallet")
    apple_card_acc = next(a for a in accounts if a.name == "Apple Card")
    chase_card_acc = next(a for a in accounts if a.name == "Chase Sapphire Card")

    logger.info("10 Accounts seeded successfully.")

    # 4. Create Investments
    investments_data = [
        {"accId": brokerage_acc.id, "sym": "AAPL", "name": "Apple Inc.", "type": "STOCK", "shares": 25.0, "buy": 165.00, "curr": 182.52},
        {"accId": brokerage_acc.id, "sym": "MSFT", "name": "Microsoft Corp.", "type": "STOCK", "shares": 15.0, "buy": 380.00, "curr": 420.55},
        {"accId": brokerage_acc.id, "sym": "VOO", "name": "Vanguard S&P 500 ETF", "type": "MUTUAL_FUND", "shares": 80.0, "buy": 395.00, "curr": 420.55},
        {"accId": brokerage_acc.id, "sym": "TSLA", "name": "Tesla Inc.", "type": "STOCK", "shares": 30.0, "buy": 190.00, "curr": 178.20},
        {"accId": retirement_acc.id, "sym": "VFFVX", "name": "Vanguard Target Retirement 2055", "type": "MUTUAL_FUND", "shares": 2000.0, "buy": 50.00, "curr": 60.00},
        {"accId": coinbase_acc.id, "sym": "BTC", "name": "Bitcoin", "type": "CRYPTO", "shares": 0.15, "buy": 55000.00, "curr": 67250.00},
        {"accId": coinbase_acc.id, "sym": "ETH", "name": "Ethereum", "type": "CRYPTO", "shares": 1.2, "buy": 2800.00, "curr": 3520.50},
        {"accId": coinbase_acc.id, "sym": "SOL", "name": "Solana", "type": "CRYPTO", "shares": 20.0, "buy": 110.00, "curr": 142.80},
    ]

    for inv in investments_data:
        await db.investment.create(
            data={
                "accountId": inv["accId"],
                "symbol": inv["sym"],
                "name": inv["name"],
                "type": inv["type"],
                "shares": inv["shares"],
                "buyPrice": inv["buy"],
                "currentPrice": inv["curr"],
                "currency": "USD"
            }
        )

    logger.info("Holdings/Investments seeded successfully.")

    # 5. Create Budgets
    today = datetime.datetime.now()
    start_date = datetime.datetime(today.year, today.month, 1)
    if today.month == 12:
        end_date = datetime.datetime(today.year + 1, 1, 1) - datetime.timedelta(seconds=1)
    else:
        end_date = datetime.datetime(today.year, today.month + 1, 1) - datetime.timedelta(seconds=1)

    categories_budgets = [
        {"cat": "FOOD", "amt": 800.0},
        {"cat": "RENT", "amt": 1800.0},
        {"cat": "UTILITIES", "amt": 300.0},
        {"cat": "ENTERTAINMENT", "amt": 400.0},
        {"cat": "TRAVEL", "amt": 600.0},
        {"cat": "OTHER", "amt": 400.0},
    ]
    for b in categories_budgets:
        await db.budget.create(
            data={
                "userId": user.id,
                "category": b["cat"],
                "amount": b["amt"],
                "period": "MONTHLY",
                "startDate": start_date,
                "endDate": end_date
            }
        )

    logger.info("Budgets seeded successfully.")

    # 6. Create Goals & Savings
    goals = [
        {"name": "Emergency Fund", "target": 15000.0, "curr": 5000.0, "days": 180},
        {"name": "Tesla Model Y Downpayment", "target": 10000.0, "curr": 2500.0, "days": 270},
        {"name": "Europe Summer Vacation", "target": 6000.0, "curr": 1200.0, "days": 90},
    ]
    for g in goals:
        goal_record = await db.goal.create(
            data={
                "userId": user.id,
                "name": g["name"],
                "targetAmount": g["target"],
                "currentAmount": g["curr"],
                "deadline": today + datetime.timedelta(days=g["days"]),
                "status": "ACTIVE"
            }
        )
        # Create savings transactions
        await db.savings.create(
            data={
                "goalId": goal_record.id,
                "amount": g["curr"] * 0.4,
                "date": today - datetime.timedelta(days=30)
            }
        )
        await db.savings.create(
            data={
                "goalId": goal_record.id,
                "amount": g["curr"] * 0.6,
                "date": today - datetime.timedelta(days=5)
            }
        )

    logger.info("Goals and Savings records seeded successfully.")

    # 7. Create Bills & Subscriptions
    bills = [
        {"name": "Comcast Internet", "amt": 89.99, "due": 5, "cat": "UTILITIES"},
        {"name": "MetLife Auto Insurance", "amt": 120.00, "due": 12, "cat": "OTHER"},
        {"name": "Electric Utility Bill", "amt": 145.50, "due": 18, "cat": "UTILITIES"},
        {"name": "Tesla Loan EMI", "amt": 450.00, "due": 25, "cat": "OTHER"},
    ]
    for bill in bills:
        await db.bill.create(
            data={
                "userId": user.id,
                "name": bill["name"],
                "amount": bill["amt"],
                "dueDate": today + datetime.timedelta(days=bill["due"]),
                "status": "UNPAID",
                "category": bill["cat"],
                "recurrence": "MONTHLY"
            }
        )

    subscriptions = [
        {"name": "Netflix Inc.", "cost": 15.49, "cycle": "MONTHLY", "due": 3, "cat": "ENTERTAINMENT"},
        {"name": "Spotify Premium", "cost": 10.99, "cycle": "MONTHLY", "due": 9, "cat": "ENTERTAINMENT"},
        {"name": "Apple One Bundle", "cost": 37.95, "cycle": "MONTHLY", "due": 15, "cat": "ENTERTAINMENT"},
        {"name": "ChatGPT Plus Subscription", "cost": 20.00, "cycle": "MONTHLY", "due": 22, "cat": "OTHER"},
    ]
    for sub in subscriptions:
        await db.subscription.create(
            data={
                "userId": user.id,
                "name": sub["name"],
                "cost": sub["cost"],
                "billingCycle": sub["cycle"],
                "nextBillingDate": today + datetime.timedelta(days=sub["due"]),
                "category": sub["cat"],
                "status": "ACTIVE"
            }
        )

    logger.info("Bills and Subscriptions seeded successfully.")

    # 8. Create Notifications
    notifications = [
        {"title": "Live Watchlist Sync", "msg": "Real-time stock feeds successfully connected.", "type": "GENERAL", "read": True, "age_days": 2},
        {"title": "Budget Alert", "msg": "You have spent 88% of your Entertainment budget limit.", "type": "ALERT", "read": False, "age_days": 1},
        {"title": "AI Savings Recommendation", "msg": "We recommend transferring $150.00 from Checking to High Yield Savings.", "type": "RECOMMENDATION", "read": False, "age_days": 0},
    ]
    for n in notifications:
        await db.notification.create(
            data={
                "userId": user.id,
                "title": n["title"],
                "message": n["msg"],
                "type": n["type"],
                "isRead": n["read"],
                "createdAt": today - datetime.timedelta(days=n["age_days"])
            }
        )

    # 9. Generate 1,000 Transactions over 12 Months
    logger.info("Generating 1,000 transactions over 12 months...")
    txs_created = 0
    target_txs = 1000

    merchants = {
        "FOOD": [
            "Whole Foods Market", "Trader Joe's", "Starbucks Coffee", "Chipotle Mexican Grill", 
            "Chopt Salad", "Shake Shack", "Local Diner", "Uber Eats Delivery", "Safeway Groceries"
        ],
        "ENTERTAINMENT": [
            "Netflix Subscription", "Spotify Premium", "AMC Movie Theater", "Steam Games", 
            "Ticketmaster Ticket", "Local Cocktail Bar", "Nintendo eShop", "Bowlero Bowling", "Comedy Club Ticket"
        ],
        "TRAVEL": [
            "Uber Ride", "Lyft Ride", "ExxonMobil Gas", "Chevron Fuel", "Delta Air Lines Flight", 
            "Airbnb Booking", "Amtrak Train Tickets", "Shell Station Gas", "NYC Transit Metro"
        ],
        "OTHER": [
            "Amazon.com Shopping", "Target Stores", "CVS Pharmacy", "Walgreens Pharmacy", 
            "Apple Store Purchase", "Nike Outlet", "Home Depot Tools", "Dry Cleaners", "UPS Shipping"
        ],
        "UTILITIES": [
            "Comcast Cable Internet", "ConEd Utility Electric", "Verizon Mobile Bill", 
            "Waste Management Services", "State Farm Renters Insurance"
        ]
    }

    # Start loop back in time (365 days ago)
    current_date = today - datetime.timedelta(days=365)
    
    while txs_created < target_txs and current_date <= today:
        day = current_date.day
        month = current_date.month

        # Income (twice a month)
        if day in [1, 15]:
            await db.transaction.create(
                data={
                    "userId": user.id,
                    "accountId": checking_acc.id,
                    "amount": 4500.00,
                    "currency": "USD",
                    "category": "SALARY",
                    "description": "Google Payroll Inflow",
                    "type": "INFLOW",
                    "status": "COMPLETED",
                    "date": current_date,
                    "source": "EMAIL"
                }
            )
            txs_created += 1

        # Rent (once a month)
        if day == 1:
            await db.transaction.create(
                data={
                    "userId": user.id,
                    "accountId": checking_acc.id,
                    "amount": 1650.00,
                    "currency": "USD",
                    "category": "RENT",
                    "description": "Lincoln Apartments Rental",
                    "type": "OUTFLOW",
                    "status": "COMPLETED",
                    "date": current_date,
                    "source": "MANUAL"
                }
            )
            txs_created += 1

        # Regular daily expenses
        daily_count = random.randint(1, 4)
        for _ in range(daily_count):
            if txs_created >= target_txs:
                break
                
            cat = random.choice(["FOOD", "FOOD", "FOOD", "ENTERTAINMENT", "TRAVEL", "OTHER"])
            desc = random.choice(merchants[cat])
            
            # Amount ranges based on category
            if cat == "FOOD":
                amount = round(random.uniform(4.50, 85.00), 2)
            elif cat == "ENTERTAINMENT":
                amount = round(random.uniform(9.99, 150.00), 2)
            elif cat == "TRAVEL":
                amount = round(random.uniform(8.00, 250.00), 2)
            else:
                amount = round(random.uniform(5.00, 180.00), 2)

            # Choose credit card or checking randomly
            acc = random.choice([checking_acc, apple_card_acc, chase_card_acc])
            
            await db.transaction.create(
                data={
                    "userId": user.id,
                    "accountId": acc.id,
                    "amount": amount,
                    "currency": "USD",
                    "category": cat,
                    "description": desc,
                    "type": "OUTFLOW",
                    "status": "COMPLETED",
                    "date": current_date + datetime.timedelta(hours=random.randint(8, 20)),
                    "source": random.choice(["MANUAL", "OCR", "SMS"])
                }
            )
            txs_created += 1

        # Increment date
        current_date += datetime.timedelta(days=1)

    # 10. Seed 2 Fraud Anomaly Transactions
    await db.transaction.create(
        data={
            "userId": user.id,
            "accountId": chase_card_acc.id,
            "amount": 1850.00,
            "currency": "USD",
            "category": "OTHER",
            "description": "Gucci Store Paris (Suspicious)",
            "type": "OUTFLOW",
            "status": "COMPLETED",
            "date": today - datetime.timedelta(hours=3),
            "source": "SMS",
            "isFraud": True
        }
    )
    
    await db.transaction.create(
        data={
            "userId": user.id,
            "accountId": apple_card_acc.id,
            "amount": 850.00,
            "currency": "USD",
            "category": "ENTERTAINMENT",
            "description": "Duplicate Ticketmaster Transaction",
            "type": "OUTFLOW",
            "status": "COMPLETED",
            "date": today - datetime.timedelta(hours=5),
            "source": "EMAIL",
            "isFraud": True
        }
    )
    txs_created += 2

    logger.info(f"Database seeding completed. Total transactions generated: {txs_created}")

if __name__ == "__main__":
    asyncio.run(seed_data())
