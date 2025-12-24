from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.instructor import Instructor
from app.repositories.base import BaseRepository


class InstructorRepository(BaseRepository[Instructor]):
    def __init__(self, db: AsyncSession):
        super().__init__(Instructor, db)
    
    async def get_by_email(self, email: str) -> Optional[Instructor]:
        """Get instructor by email"""
        result = await self.db.execute(
            select(Instructor).where(Instructor.email.ilike(email.lower()))
        )
        return result.scalar_one_or_none()
    
    async def get_by_department(
        self,
        department_id: UUID,
        include_inactive: bool = False
    ) -> List[Instructor]:
        """Get instructors in department"""
        query = select(Instructor).where(Instructor.home_department_id == department_id)
        if not include_inactive:
            query = query.where(Instructor.is_active == True)
        
        result = await self.db.execute(
            query.options(selectinload(Instructor.home_department))
        )
        return list(result.scalars().all())
    
    async def get_active_instructors_for_term(self, term_id: UUID) -> List[Instructor]:
        """Get all active instructors for a specific term"""
        # This would need a join with availability or course offerings
        # For now, return all active instructors
        result = await self.db.execute(
            select(Instructor).where(Instructor.is_active == True)
        )
        return list(result.scalars().all())

