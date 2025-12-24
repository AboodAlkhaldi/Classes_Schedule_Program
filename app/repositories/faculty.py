from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.faculty import Faculty
from app.repositories.base import BaseRepository


class FacultyRepository(BaseRepository[Faculty]):
    def __init__(self, db: AsyncSession):
        super().__init__(Faculty, db)
    
    async def get_by_code(self, code: str) -> Optional[Faculty]:
        """Get faculty by code"""
        return await self.get_by_field("code", code.upper())
    
    async def get_by_name(self, name: str) -> Optional[Faculty]:
        """Get faculty by name"""
        result = await self.db.execute(
            select(Faculty).where(Faculty.name.ilike(f"%{name}%"))
        )
        return result.scalar_one_or_none()

