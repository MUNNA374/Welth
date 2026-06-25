from typing import Optional
import logging
from backend.app.core.db import db

logger = logging.getLogger("welth.security.audit")

async def log_audit_event(
    action: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[str] = None
) -> None:
    """Log security-critical operations to the database and standard output."""
    try:
        if db.is_connected():
            await db.auditlog.create(
                data={
                    "userId": user_id,
                    "action": action,
                    "ipAddress": ip_address,
                    "userAgent": user_agent,
                    "details": details
                }
            )
        logger.info(f"AUDIT LOG: Action='{action}', User='{user_id or 'System'}', Details='{details or ''}'")
    except Exception as e:
        logger.error(f"Failed to save audit log: {e}")
        # Log to stdout at least as fallback
        logger.info(f"FALLBACK AUDIT LOG: Action='{action}', User='{user_id or 'System'}', Details='{details or ''}'")
