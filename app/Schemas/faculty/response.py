from uuid import UUID
from datetime import datetime
from app.schemas.faculty.base import FacultyBase
from app.schemas.base import BaseSchema


class FacultyResponse(FacultyBase, BaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class FacultyListResponse(BaseSchema):
    items: list[FacultyResponse]
    total: int
    page: int
    page_size: int


