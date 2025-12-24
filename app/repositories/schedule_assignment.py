from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from app.models.schedule_assignment import ScheduleAssignment
from app.repositories.base import BaseRepository


class ScheduleAssignmentRepository(BaseRepository[ScheduleAssignment]):
    def __init__(self, db: AsyncSession):
        super().__init__(ScheduleAssignment, db)
    
    async def get_by_schedule(self, schedule_id: UUID) -> List[ScheduleAssignment]:
        """Get all assignments for schedule"""
        result = await self.db.execute(
            select(ScheduleAssignment)
            .where(ScheduleAssignment.schedule_id == schedule_id)
            .options(
                selectinload(ScheduleAssignment.course_offering),
                selectinload(ScheduleAssignment.time_slot),
                selectinload(ScheduleAssignment.classroom)
            )
        )
        return list(result.scalars().all())
    
    async def check_instructor_conflict(
        self,
        instructor_id: UUID,
        time_slot_id: UUID,
        schedule_id: UUID,
        exclude_assignment_id: Optional[UUID] = None
    ) -> bool:
        """Check if instructor has conflict at time slot"""
        from app.models.course_offering import CourseOffering
        
        # Check if instructor is teaching another course at the same time slot
        query = select(ScheduleAssignment).join(CourseOffering).where(
            and_(
                CourseOffering.instructor_id == instructor_id,
                ScheduleAssignment.time_slot_id == time_slot_id,
                ScheduleAssignment.schedule_id == schedule_id
            )
        )
        
        if exclude_assignment_id:
            query = query.where(ScheduleAssignment.id != exclude_assignment_id)
        
        result = await self.db.execute(query)
        conflicting = result.scalar_one_or_none()
        return conflicting is not None
    
    async def check_classroom_conflict(
        self,
        classroom_id: UUID,
        time_slot_id: UUID,
        schedule_id: UUID,
        exclude_assignment_id: Optional[UUID] = None
    ) -> bool:
        """Check if classroom has conflict at time slot"""
        query = select(ScheduleAssignment).where(
            and_(
                ScheduleAssignment.classroom_id == classroom_id,
                ScheduleAssignment.time_slot_id == time_slot_id,
                ScheduleAssignment.schedule_id == schedule_id
            )
        )
        
        if exclude_assignment_id:
            query = query.where(ScheduleAssignment.id != exclude_assignment_id)
        
        result = await self.db.execute(query)
        conflicting = result.scalar_one_or_none()
        return conflicting is not None

