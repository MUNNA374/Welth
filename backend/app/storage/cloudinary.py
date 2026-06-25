import logging
from typing import Optional
from backend.app.core.config import settings

logger = logging.getLogger("welth.storage.cloudinary")

try:
    import cloudinary
    import cloudinary.uploader
    cloudinary_available = True
    if settings.CLOUDINARY_URL:
        cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL)
except ImportError:
    cloudinary_available = False

async def upload_image_to_cloudinary(file_path: str) -> Optional[str]:
    """Upload an image to Cloudinary. Returns the secure URL if successful."""
    if not cloudinary_available or not settings.CLOUDINARY_URL:
        logger.info("Cloudinary not configured. Skipping Cloudinary upload.")
        return None

    try:
        response = cloudinary.uploader.upload(file_path, folder="welth_receipts")
        secure_url = response.get("secure_url")
        logger.info(f"Image uploaded to Cloudinary successfully: {secure_url}")
        return secure_url
    except Exception as e:
        logger.error(f"Cloudinary upload error: {e}")
        return None
