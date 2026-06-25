import asyncio
import logging
import datetime
from backend.app.core.db import db, init_db, close_db
from backend.app.security.jwt import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("welth.seed")

async def seed_data():
    logger.info("Starting database seeding...")
    await init_db()
    
    # 1. Clear existing data (optional, but good for clean seed runs)
    # We do this using Prisma delete_many operations
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

    # 3. Create Accounts
    checking = await db.account.create(
        data={
            "userId": user.id,
            "name": "Chase Checking",
            "type": "BANK",
            "balance": 5420.50,
            "currency": "USD",
            "institution": "Chase Bank"
        }
    )
    
    brokerage = await db.account.create(
        data={
            "userId": user.id,
            "name": "Fidelity Brokerage",
            "type": "INVESTMENT",
            "balance": 24500.00,
            "currency": "USD",
            "institution": "Fidelity Investments"
        }
    )
    
    credit_card = await db.account.create(
        data={
            "userId": user.id,
            "name": "Apple Card",
            "type": "CREDIT",
            "balance": -1200.00,
            "currency": "USD",
            "institution": "Goldman Sachs"
        }
    )
    
    logger.info("Accounts seeded successfully.")

    # 4. Create Investments
    await db.investment.create(
        data={
            "accountId": brokerage.id,
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "type": "STOCK",
            "shares": 10.0,
            "buyPrice": 175.00,
            "currentPrice": 182.52,
            "currency": "USD"
        }
    )

    await db.investment.create(
        data={
            "accountId": brokerage.id,
            "symbol": "VOO",
            "name": "Vanguard S&P 500 ETF",
            "type": "MUTUAL_FUND",
            "shares": 40.0,
            "buyPrice": 410.00,
            "currentPrice": 420.55,
            "currency": "USD"
        }
    )

    logger.info("Investments seeded successfully.")

    # 5. Create Budgets
    today = datetime.datetime.now()
    start_date = datetime.datetime(today.year, today.month, 1)
    # Next month's 1st day minus 1 sec
    if today.month == 12:
        end_date = datetime.datetime(today.year + 1, 1, 1) - datetime.timedelta(seconds=1)
    else:
        end_date = datetime.datetime(today.year, today.month + 1, 1) - datetime.timedelta(seconds=1)

    await db.budget.create(
        data={
            "userId": user.id,
            "category": "FOOD",
            "amount": 600.0,
            "period": "MONTHLY",
            "startDate": start_date,
            "endDate": end_date
        }
    )

    await db.budget.create(
        data={
            "userId": user.id,
            "category": "ENTERTAINMENT",
            "amount": 250.0,
            "period": "MONTHLY",
            "startDate": start_date,
            "endDate": end_date
        }
    )
    
    logger.info("Budgets seeded successfully.")

    # 6. Create Bills & Subscriptions
    await db.bill.create(
        data={
            "userId": user.id,
            "name": "Comcast Cable Internet",
            "amount": 89.99,
            "dueDate": today + datetime.timedelta(days=5),
            "status": "UNPAID",
            "category": "UTILITIES",
            "recurrence": "MONTHLY"
        }
    )

    await db.bill.create(
        data={
            "userId": user.id,
            "name": "MetLife Auto Insurance",
            "amount": 115.00,
            "dueDate": today + datetime.timedelta(days=12),
            "status": "UNPAID",
            "category": "OTHER",
            "recurrence": "MONTHLY"
        }
    )

    await db.subscription.create(
        data={
            "userId": user.id,
            "name": "Netflix Inc.",
            "cost": 15.49,
            "billingCycle": "MONTHLY",
            "nextBillingDate": today + datetime.timedelta(days=3),
            "category": "ENTERTAINMENT",
            "status": "ACTIVE"
        }
    )

    logger.info("Bills & Subscriptions seeded successfully.")

    # 7. Create Goals & Savings
    goal = await db.goal.create(
        data={
            "userId": user.id,
            "name": "Emergency Fund",
            "targetAmount": 10000.0,
            "currentAmount": 3000.0,
            "deadline": today + datetime.timedelta(days=365),
            "status": "ACTIVE"
        }
    )

    await db.savings.create(
        data={
            "goalId": goal.id,
            "amount": 500.0,
            "date": today - datetime.timedelta(days=10)
        }
    )

    logger.info("Goals and Savings seeded successfully.")

    # 8. Create Transactions
    transactions = [
        # Income
        {"desc": "Google Payroll Inflow", "amount": 6200.00, "cat": "SALARY", "type": "INFLOW", "days_ago": 25},
        # Regular Rent
        {"desc": "Lincoln Apartments Rental", "amount": 1650.00, "cat": "RENT", "type": "OUTFLOW", "days_ago": 24},
        # Food
        {"desc": "Whole Foods Market", "amount": 142.10, "cat": "FOOD", "type": "OUTFLOW", "days_ago": 20},
        {"desc": "Trader Joe's Grocery", "amount": 88.50, "cat": "FOOD", "type": "OUTFLOW", "days_ago": 15},
        {"desc": "Starbucks Coffee", "amount": 6.80, "cat": "FOOD", "type": "OUTFLOW", "days_ago": 12},
        # Utilities
        {"desc": "ConEd Utility Electric", "amount": 115.40, "cat": "UTILITIES", "type": "OUTFLOW", "days_ago": 18},
        # Entertainment
        {"desc": "Netflix Subscription Billing", "amount": 15.49, "cat": "ENTERTAINMENT", "type": "OUTFLOW", "days_ago": 25},
        {"desc": "AMC Theater Movies", "amount": 42.00, "cat": "ENTERTAINMENT", "type": "OUTFLOW", "days_ago": 10},
        # Investment Transfer
        {"desc": "Wire to Fidelity ETF VOO", "amount": 500.00, "cat": "INVESTMENT", "type": "OUTFLOW", "days_ago": 5}
    ]

    for tx in transactions:
        await db.transaction.create(
            data={
                "userId": user.id,
                "accountId": checking.id if tx["type"] == "INFLOW" or tx["cat"] == "RENT" else credit_card.id,
                "amount": tx["amount"],
                "currency": "USD",
                "category": tx["cat"],
                "description": tx["desc"],
                "type": tx["type"],
                "status": "COMPLETED",
                "date": today - datetime.timedelta(days=tx["days_ago"]),
                "source": "MANUAL"
            }
        )

    logger.info("Transactions seeded successfully.")
    logger.info("Database seeding completed.")

if __name__ == "__main__":
    asyncio.run(seed_data())
