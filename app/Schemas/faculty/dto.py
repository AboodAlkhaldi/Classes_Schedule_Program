from pydantic import BaseModel
from app.schemas.faculty.base import FacultyBase


class FacultyCreate(FacultyBase):
    """Used when creating a new faculty"""
    pass


class FacultyUpdate(BaseModel):
    """Used for updates - all fields optional"""
    code: str | None = None
    name: str | None = None

