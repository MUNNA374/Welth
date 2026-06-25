from typing import Optional, Any
from backend.app.repositories.user_repository import UserRepository
from backend.app.core.db import db

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def get_user_profile(self, user_id: str) -> Any:
        return await self.user_repo.get(user_id)

    async def get_user_settings(self, user_id: str) -> Any:
        return await db.settings.find_unique(where={"userId": user_id})

    async def update_user_settings(self, user_id: str, settings_data: dict) -> Any:
        return await db.settings.update(
            where={"userId": user_id},
            data=settings_data
        )
