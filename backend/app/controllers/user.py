from fastapi import APIRouter, Depends
from backend.app.services.user_service import UserService
from backend.app.api.deps import get_current_user
from pydantic import BaseModel
from typing import Optional, Any

router = APIRouter()
user_service = UserService()

class SettingsUpdate(BaseModel):
    theme: Optional[str] = None
    currency: Optional[str] = None
    emailNotifications: Optional[bool] = None
    smsNotifications: Optional[bool] = None
    pushNotifications: Optional[bool] = None

@router.get("/profile")
async def get_profile(current_user: Any = Depends(get_current_user)):
    profile = await user_service.get_user_profile(current_user.id)
    return profile

@router.get("/settings")
async def get_settings(current_user: Any = Depends(get_current_user)):
    settings = await user_service.get_user_settings(current_user.id)
    return settings

@router.put("/settings")
async def update_settings(settings_in: SettingsUpdate, current_user: Any = Depends(get_current_user)):
    cleaned_data = {k: v for k, v in settings_in.model_dump().items() if v is not None}
    updated = await user_service.update_user_settings(current_user.id, cleaned_data)
    return updated
