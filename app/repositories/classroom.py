from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.models.classroom import Classroom
from app.repositories.base import BaseRepository


class ClassroomRepository(BaseRepository[Classroom]):
    def __init__(self, db: AsyncSession):
        super().__init__(Classroom, db)
    
    async def get_by_code(self, code: str) -> Optional[Classroom]:
        """Get classroom by code"""
        return await self.get_by_field("code", code)
    
    async def get_by_department(
        self,
        department_id: UUID,
        classroom_type: Optional[str] = None
    ) -> List[Classroom]:
        """Get classrooms by department and optionally by type"""
        query = select(Classroom).where(Classroom.department_id == department_id)
        if classroom_type:
            query = query.where(Classroom.classroom_type == classroom_type)
        
        result = await self.db.execute(
            query.options(selectinload(Classroom.department))
        )
        return list(result.scalars().all())
    
    async def get_available_classrooms(
        self,
        time_slot_id: UUID,
        schedule_id: UUID,
        min_capacity: int,
        classroom_type: Optional[str] = None,
        required_features: Optional[Dict[str, Any]] = None
    ) -> List[Classroom]:
        """Get classrooms available at specific time slot"""
        # This is a simplified version - full implementation would check schedule_assignments
        query = select(Classroom).where(
            and_(
                Classroom.is_active == True,
                Classroom.capacity >= min_capacity
            )
        )
        
        if classroom_type:
            query = query.where(Classroom.classroom_type == classroom_type)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())

