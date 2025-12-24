from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.course_offering import CourseOffering
from app.repositories.base import BaseRepository


class CourseOfferingRepository(BaseRepository[CourseOffering]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseOffering, db)

