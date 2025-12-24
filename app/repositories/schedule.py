from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.models.schedule import Schedule
from app.core.constants import ScheduleStatus
from app.repositories.base import BaseRepository


class ScheduleRepository(BaseRepository[Schedule]):
    def __init__(self, db: AsyncSession):
        super().__init__(Schedule, db)
    
    async def get_by_term_and_department(
        self,
        term_id: UUID,
        department_id: UUID
    ) -> Optional[Schedule]:
        """Get schedule for term and department"""
        result = await self.db.execute(
            select(Schedule)
            .where(and_(
                Schedule.term_id == term_id,
                Schedule.department_id == department_id
            ))
            .options(
                selectinload(Schedule.term),
                selectinload(Schedule.department),
                selectinload(Schedule.assignments)
            )
        )
        return result.scalar_one_or_none()
    
    async def get_schedules_by_status(
        self,
        status: ScheduleStatus,
        department_id: Optional[UUID] = None
    ) -> List[Schedule]:
        """Get schedules filtered by status"""
        query = select(Schedule).where(Schedule.status == status)
        
        if department_id:
            query = query.where(Schedule.department_id == department_id)
        
        result = await self.db.execute(
            query.options(
                selectinload(Schedule.term),
                selectinload(Schedule.department)
            )
        )
        return list(result.scalars().all())
    
    async def submit_schedule(self, schedule_id: UUID, user_id: UUID) -> Optional[Schedule]:
        """Submit schedule for approval"""
        return await self.update(schedule_id, {
            "status": ScheduleStatus.PENDING_APPROVAL,
            "submitted_at": datetime.utcnow(),
            "submitted_by": user_id
        })
    
    async def approve_schedule(
        self,
        schedule_id: UUID,
        user_id: UUID
    ) -> Optional[Schedule]:
        """Approve schedule"""
        return await self.update(schedule_id, {
            "status": ScheduleStatus.APPROVED,
            "evaluated_at": datetime.utcnow(),
            "evaluated_by": user_id
        })
    
    async def reject_schedule(
        self,
        schedule_id: UUID,
        user_id: UUID
    ) -> Optional[Schedule]:
        """Reject schedule"""
        return await self.update(schedule_id, {
            "status": ScheduleStatus.REJECTED,
            "evaluated_at": datetime.utcnow(),
            "evaluated_by": user_id
        })

