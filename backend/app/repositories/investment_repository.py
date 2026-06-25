from typing import List, Any
from backend.app.repositories.base import BaseRepository

class InvestmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(model_name="Investment")

    async def get_by_account(self, account_id: str) -> List[Any]:
        return await self.delegate.find_many(where={"accountId": account_id})
