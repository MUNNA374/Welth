import os
import logging
from typing import Optional
from fastapi import UploadFile
from backend.app.core.config import settings

logger = logging.getLogger("welth.storage.s3")

# Try importing boto3, log if not installed
try:
    import boto3
    from botocore.exceptions import NoCredentialsError
    boto3_available = True
except ImportError:
    boto3_available = False

async def upload_to_s3(file_path: str, destination_name: str) -> Optional[str]:
    """Upload a local file to S3 bucket. Return the public URL if successful."""
    if not boto3_available or not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        logger.info("S3 storage not configured. Skipping S3 upload.")
        return None

    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        s3.upload_file(file_path, settings.AWS_S3_BUCKET_NAME, destination_name)
        # Construct S3 URL
        s3_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{destination_name}"
        logger.info(f"File uploaded to S3 successfully: {s3_url}")
        return s3_url
    except NoCredentialsError:
        logger.error("AWS S3 Credentials not found.")
        return None
    except Exception as e:
        logger.error(f"S3 upload error: {e}")
        return None
