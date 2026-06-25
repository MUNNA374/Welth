import logging
from typing import Optional
from backend.app.core.config import settings

logger = logging.getLogger("welth.notifications.sms")

async def send_sms(to_phone: str, message: str) -> bool:
    """Send an SMS message (mocked Twilio/SNS by default)."""
    logger.info(f"SMS SENT TO: {to_phone} | MESSAGE: '{message}'")
    return True
