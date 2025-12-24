from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.schemas.user.dto import UserCreate, UserUpdate
from app.schemas.user.response import UserResponse, UserListResponse
from app.utils.normalization import normalize_email


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create new user"""
        from app.core.security import hash_password
        
        # Normalize email
        email = normalize_email(user_data.email)
        
        # Check if user exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("User with this email already exists")
        
        # Hash password and create user
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["email"] = email
        user_dict["password_hash"] = hash_password(user_data.password)
        user = await self.user_repo.create(user_dict)
        return UserResponse.model_validate(user)
    
    async def get_user(self, user_id: UUID) -> Optional[UserResponse]:
        """Get user by ID"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    async def get_users(
        self,
        skip: int = 0,
        limit: int = 50,
        filters: Optional[dict] = None
    ) -> UserListResponse:
        """Get list of users"""
        users = await self.user_repo.get_multi(skip=skip, limit=limit, filters=filters)
        total = await self.user_repo.count(filters=filters)
        
        return UserListResponse(
            items=[UserResponse.model_validate(u) for u in users],
            total=total,
            page=(skip // limit) + 1,
            page_size=limit
        )
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[UserResponse]:
        """Update user"""
        update_dict = user_data.model_dump(exclude_unset=True)
        
        # Normalize email if provided
        if "email" in update_dict:
            update_dict["email"] = normalize_email(update_dict["email"])
        
        user = await self.user_repo.update(user_id, update_dict)
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    async def delete_user(self, user_id: UUID) -> bool:
        """Delete user"""
        return await self.user_repo.delete(user_id)
    
    async def deactivate_user(self, user_id: UUID) -> Optional[UserResponse]:
        """Deactivate user"""
        user = await self.user_repo.update(user_id, {"is_active": False})
        if not user:
            return None
        return UserResponse.model_validate(user)
    
    async def activate_user(self, user_id: UUID) -> Optional[UserResponse]:
        """Activate user"""
        user = await self.user_repo.update(user_id, {"is_active": True})
        if not user:
            return None
        return UserResponse.model_validate(user)


