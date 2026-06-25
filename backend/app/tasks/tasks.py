import asyncio
import logging
from backend.app.tasks.celery_app import celery_app
from backend.app.core.db import db, init_db, close_db
from backend.app.ai.gemini_client import GeminiClient
from backend.app.notifications.in_app import create_in_app_notification
from backend.app.services.fetchers.email import EmailTransactionParserFetcher
from backend.app.services.fetchers.sms import SMSTransactionParserFetcher

logger = logging.getLogger("welth.tasks")

async def run_async(coro):
    """Utility wrapper to connect to DB, run async coroutine, and close DB."""
    try:
        await init_db()
        return await coro
    finally:
        await close_db()

# 1. Receipt OCR Task
async def _process_receipt_ocr(receipt_id: str):
    logger.info(f"Starting async OCR processing for Receipt {receipt_id}")
    receipt = await db.receipt.find_unique(where={"id": receipt_id})
    if not receipt:
        logger.error(f"Receipt {receipt_id} not found.")
        return
        
    try:
        # Call Gemini receipt parsing
        ai = GeminiClient()
        ocr_result = await ai.parse_receipt_ocr(f"OCR File URL: {receipt.filePath}")
        
        # Update receipt record
        import datetime
        await db.receipt.update(
            where={"id": receipt_id},
            data={
                "parsedAmount": float(ocr_result.get("total_amount", 0.0)),
                "parsedMerchant": ocr_result.get("merchant", "Unknown Merchant"),
                "parsedDate": datetime.datetime.fromisoformat(ocr_result.get("date", datetime.date.today().isoformat())),
                "status": "PROCESSED"
            }
        )
        # Create In-App Notification
        await create_in_app_notification(
            user_id=receipt.userId,
            title="Receipt Processed",
            message=f"Receipt from {ocr_result.get('merchant')} of amount {ocr_result.get('total_amount')} has been parsed.",
            notification_type="GENERAL"
        )
    except Exception as e:
        logger.error(f"Receipt OCR task failed: {e}")
        await db.receipt.update(
            where={"id": receipt_id},
            data={"status": "FAILED"}
        )

@celery_app.task(name="process_receipt_ocr_task")
def process_receipt_ocr_task(receipt_id: str):
    return asyncio.run(run_async(_process_receipt_ocr(receipt_id)))


# 2. Email & SMS Parsers
async def _parse_email_transactions(user_id: str):
    parser = EmailTransactionParserFetcher()
    emails = await parser.parse_emails(user_id)
    
    # Simulating insertion of email parsed transactions into DB
    for em in emails:
        # Grab first account for user
        acc = await db.account.find_first(where={"userId": user_id})
        if not acc:
            continue
            
        await db.transaction.create(
            data={
                "userId": user_id,
                "accountId": acc.id,
                "amount": float(em["amount"]),
                "category": em["category"],
                "description": f"Email Parse: {em['merchant']}",
                "type": "OUTFLOW",
                "source": "EMAIL"
            }
        )
    logger.info(f"Email parser task finished for user {user_id}. Found {len(emails)} transactions.")

@celery_app.task(name="parse_email_transactions_task")
def parse_email_transactions_task(user_id: str):
    return asyncio.run(run_async(_parse_email_transactions(user_id)))


async def _parse_sms_transactions(user_id: str):
    parser = SMSTransactionParserFetcher()
    sms_list = await parser.parse_sms(user_id)
    
    for sm in sms_list:
        acc = await db.account.find_first(where={"userId": user_id})
        if not acc:
            continue
            
        await db.transaction.create(
            data={
                "userId": user_id,
                "accountId": acc.id,
                "amount": float(sm["amount"]),
                "category": sm["category"],
                "description": f"SMS Parse: {sm['merchant']}",
                "type": "OUTFLOW",
                "source": "SMS"
            }
        )
    logger.info(f"SMS parser task finished for user {user_id}. Found {len(sms_list)} transactions.")

@celery_app.task(name="parse_sms_transactions_task")
def parse_sms_transactions_task(user_id: str):
    return asyncio.run(run_async(_parse_sms_transactions(user_id)))


# 3. Bill Reminders Task (checks upcoming bills)
async def _send_bill_reminders():
    import datetime
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    
    # Grab all unpaid bills due before tomorrow
    bills = await db.bill.find_many(
        where={
            "status": "UNPAID",
            "dueDate": {"lte": tomorrow}
        }
    )
    
    for bill in bills:
        await create_in_app_notification(
            user_id=bill.userId,
            title="Upcoming Bill Reminder",
            message=f"Your bill '{bill.name}' of amount {bill.amount:.2f} is due by {bill.dueDate.date()}.",
            notification_type="ALERT"
        )
    logger.info(f"Bill reminder task executed. Sent alerts for {len(bills)} bills.")

@celery_app.task(name="send_bill_reminders_task")
def send_bill_reminders_task():
    return asyncio.run(run_async(_send_bill_reminders()))
