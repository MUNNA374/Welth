from typing import Generic, TypeVar, List, Optional, Any, Dict
from backend.app.core.db import db

class BaseRepository:
    """Generic Base Repository exposing CRUD functions via Prisma."""
    def __init__(self, model_name: str):
        self.model_name = model_name

    @property
    def delegate(self):
        """Dynamic access to the Prisma model delegate (e.g., db.user)."""
        return getattr(db, self.model_name.lower())

    async def get(self, id: str) -> Optional[Any]:
        """Find a single record by its UUID."""
        return await self.delegate.find_unique(where={"id": id})

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """Retrieve multiple records with pagination."""
        return await self.delegate.find_many(skip=skip, take=limit)

    async def create(self, data: Dict[str, Any]) -> Any:
        """Create a new record."""
        return await self.delegate.create(data=data)

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Any]:
        """Update an existing record."""
        return await self.delegate.update(where={"id": id}, data=data)

    async def delete(self, id: str) -> Optional[Any]:
        """Delete a record by UUID."""
        return await self.delegate.delete(where={"id": id})
