from typing import List, Any
from backend.app.repositories.base import BaseRepository

class BudgetRepository(BaseRepository):
    def __init__(self):
        super().__init__(model_name="Budget")

    async def get_user_budgets(self, user_id: str) -> List[Any]:
        return await self.delegate.find_many(where={"userId": user_id})
