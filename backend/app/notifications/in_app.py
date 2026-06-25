import logging
from typing import Optional
from backend.app.core.db import db

logger = logging.getLogger("welth.notifications.in_app")

async def create_in_app_notification(user_id: str, title: str, message: str, notification_type: str = "GENERAL") -> bool:
    """Save a notification record to the database for retrieval by the client."""
    try:
        if db.is_connected():
            await db.notification.create(
                data={
                    "userId": user_id,
                    "title": title,
                    "message": message,
                    "type": notification_type,
                    "isRead": False
                }
            )
            logger.info(f"In-App Notification created for user {user_id}: {title}")
            return True
    except Exception as e:
        logger.error(f"Failed to create in-app notification: {e}")
    return False
