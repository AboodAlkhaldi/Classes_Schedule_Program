from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.user.base import UserBase
from app.schemas.base import BaseSchema


class UserResponse(UserBase, BaseSchema):
    id: UUID
    department_id: Optional[UUID]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseSchema):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int


