import os
import uuid
import shutil
import logging
from fastapi import UploadFile
from backend.app.storage.aws_s3 import upload_to_s3
from backend.app.storage.cloudinary import upload_image_to_cloudinary

logger = logging.getLogger("welth.storage.uploads")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    """Save an uploaded file, sync with remote cloud storage if configured, and return access URL."""
    # 1. Generate unique file name
    file_extension = os.path.splitext(file.filename)[-1] if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    local_path = os.path.join(UPLOAD_DIR, unique_filename)

    # 2. Write file content to local storage
    try:
        with open(local_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File saved locally: {local_path}")
    except Exception as e:
        logger.error(f"Failed to write file locally: {e}")
        raise

    # 3. Attempt image upload to Cloudinary (if receipt/image)
    if file_extension.lower() in [".png", ".jpg", ".jpeg", ".webp"]:
        cloudinary_url = await upload_image_to_cloudinary(local_path)
        if cloudinary_url:
            return cloudinary_url

    # 4. Attempt document upload to S3
    s3_url = await upload_to_s3(local_path, unique_filename)
    if s3_url:
        return s3_url

    # 5. Default back to local reference path
    return f"/static/uploads/{unique_filename}"
