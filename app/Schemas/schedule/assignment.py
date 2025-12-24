from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.schemas.base import BaseSchema


class ScheduleAssignmentCreate(BaseModel):
    course_offering_id: UUID
    time_slot_id: UUID
    classroom_id: UUID


class ScheduleAssignmentResponse(ScheduleAssignmentCreate, BaseSchema):
    id: UUID
    schedule_id: UUID
    created_at: datetime


class ScheduleAssignmentDetail(ScheduleAssignmentResponse):
    """Extended with related entities"""
    pass


