from pydantic import BaseModel, Field


class FacultyBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=3, pattern="^[A-Z]{3}$")
    name: str = Field(..., min_length=1, max_length=50)


