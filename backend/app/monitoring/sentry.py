import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from backend.app.core.config import settings

def init_sentry() -> None:
    """Initialize Sentry SDK if DSN is set in settings."""
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            integrations=[
                FastApiIntegration(),
            ],
        )
