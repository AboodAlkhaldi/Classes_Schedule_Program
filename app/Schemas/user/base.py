from pydantic import BaseModel, EmailStr, Field
from app.core.constants import UserRole


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: UserRole


