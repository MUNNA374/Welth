import logging
from typing import Optional
from backend.app.core.config import settings

logger = logging.getLogger("welth.notifications.email")

async def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an email notification via SMTP (mocked by default)."""
    logger.info(f"EMAIL SENT TO: {to_email} | SUBJECT: '{subject}'")
    # In a production context, standard smtplib/email modules or Sendgrid/SES client is used.
    # We will log the email dispatch successfully.
    return True
