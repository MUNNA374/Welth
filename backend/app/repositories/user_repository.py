from typing import Optional, Any
from backend.app.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model_name="User")

    async def get_by_email(self, email: str) -> Optional[Any]:
        return await self.delegate.find_unique(where={"email": email})
