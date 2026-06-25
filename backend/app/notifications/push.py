import logging
from typing import Optional
from backend.app.core.config import settings

logger = logging.getLogger("welth.notifications.push")

async def send_push_notification(user_id: str, title: str, body: str) -> bool:
    """Send a push notification via WebPush/FCM (mocked by default)."""
    logger.info(f"PUSH NOTIFICATION SENT TO USER: {user_id} | TITLE: '{title}' | BODY: '{body}'")
    return True
