from typing import List
from uuid import UUID
from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.models.time_slot import TimeSlot
from app.core.constants import DayOfWeek
from app.repositories.base import BaseRepository


class TimeSlotRepository(BaseRepository[TimeSlot]):
    def __init__(self, db: AsyncSession):
        super().__init__(TimeSlot, db)
    
    async def get_by_term(self, term_id: UUID) -> List[TimeSlot]:
        """Get all time slots for term"""
        result = await self.db.execute(
            select(TimeSlot)
            .where(TimeSlot.term_id == term_id)
            .options(selectinload(TimeSlot.term))
        )
        return list(result.scalars().all())
    
    async def get_by_day(
        self,
        term_id: UUID,
        day_of_week: DayOfWeek
    ) -> List[TimeSlot]:
        """Get time slots for specific day"""
        result = await self.db.execute(
            select(TimeSlot)
            .where(and_(
                TimeSlot.term_id == term_id,
                TimeSlot.day_of_week == day_of_week
            ))
            .order_by(TimeSlot.start_time)
        )
        return list(result.scalars().all())

