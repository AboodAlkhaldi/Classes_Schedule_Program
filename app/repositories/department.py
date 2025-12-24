from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.department import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: AsyncSession):
        super().__init__(Department, db)
    
    async def get_by_code(self, code: str, faculty_id: Optional[UUID] = None) -> Optional[Department]:
        """Get department by code, optionally filtered by faculty"""
        query = select(Department).where(Department.code == code.upper())
        if faculty_id:
            query = query.where(Department.faculty_id == faculty_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_faculty(self, faculty_id: UUID) -> List[Department]:
        """Get all departments for a faculty"""
        result = await self.db.execute(
            select(Department)
            .where(Department.faculty_id == faculty_id)
            .options(selectinload(Department.faculty))
        )
        return list(result.scalars().all())

