from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.schedule.base import ScheduleBase
from app.schemas.base import BaseSchema
from app.core.constants import ScheduleStatus


class ScheduleResponse(ScheduleBase, BaseSchema):
    id: UUID
    status: ScheduleStatus
    submitted_at: Optional[datetime]
    submitted_by: UUID
    evaluated_at: Optional[datetime]
    evaluated_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime


class ScheduleDetailResponse(ScheduleResponse):
    """Full schedule with all assignments"""
    assignments: List[dict]  # Will be ScheduleAssignmentDetail
    review_notes: List[dict]  # Will be ReviewNoteResponse


