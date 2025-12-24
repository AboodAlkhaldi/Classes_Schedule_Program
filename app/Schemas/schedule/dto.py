from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from app.schemas.schedule.base import ScheduleBase


class ScheduleCreate(ScheduleBase):
    """Create new schedule"""
    pass


class ScheduleSubmit(BaseModel):
    """Used when submitting for approval"""
    notes: Optional[str] = None


class ScheduleApproval(BaseModel):
    """Used when approving or rejecting"""
    approved: bool
    notes: str = Field(..., min_length=1)


