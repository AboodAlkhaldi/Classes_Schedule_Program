from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)


class IDSchema(BaseSchema):
    """Schema with just ID"""
    id: UUID


class TimestampSchema(BaseSchema):
    """Schema with timestamps"""
    created_at: datetime
    updated_at: datetime


