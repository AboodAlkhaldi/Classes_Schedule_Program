from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email (case-insensitive)"""
        result = await self.db.execute(
            select(User).where(User.email.ilike(email.lower()))
        )
        return result.scalar_one_or_none()
    
    async def get_active_users_by_department(self, department_id: UUID) -> list[User]:
        """Get all active users in a department"""
        result = await self.db.execute(
            select(User)
            .where(and_(User.department_id == department_id, User.is_active == True))
            .options(selectinload(User.department))
        )
        return list(result.scalars().all())

