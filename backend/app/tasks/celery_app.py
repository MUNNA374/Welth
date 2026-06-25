from celery import Celery
from backend.app.core.config import settings

# Initialize Celery using Redis as both the message broker and result backend
celery_app = Celery(
    "welth_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["backend.app.tasks.tasks"]
)

# Optional configurations for task serialization and concurrency limits
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1
)
