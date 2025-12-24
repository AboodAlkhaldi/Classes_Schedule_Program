import re
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from app.schemas.user.base import UserBase
from app.core.constants import UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    department_id: Optional[UUID] = None
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Password must contain uppercase, lowercase, and digit"""
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', v):
            raise ValueError('Password must contain uppercase, lowercase, and digit')
        return v
    
    @model_validator(mode='after')
    def validate_department_for_role(self):
        if self.role in [UserRole.DEAN, UserRole.DEPARTMENT_REP] and not self.department_id:
            raise ValueError(f'{self.role} must have department_id')
        return self


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = None
    department_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class PasswordReset(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', v):
            raise ValueError('Password must contain uppercase, lowercase, and digit')
        return v


