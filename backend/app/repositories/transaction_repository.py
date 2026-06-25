from typing import List, Any
from backend.app.repositories.base import BaseRepository

class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(model_name="Transaction")

    async def get_by_user(self, user_id: str, limit: int = 100) -> List[Any]:
        return await self.delegate.find_many(
            where={"userId": user_id},
            order={"date": "desc"},
            take=limit
        )

    async def get_by_account(self, account_id: str) -> List[Any]:
        return await self.delegate.find_many(where={"accountId": account_id})
