from uuid import UUID
from datetime import timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.auth.register import RegisterRequest, RegisterResponse
from app.schemas.user.dto import UserCreate
from app.schemas.user.response import UserResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db
    
    async def register_user(self, user_data: RegisterRequest) -> RegisterResponse:
        """Register new user with password hashing"""
        # Check if user exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create user
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password_hash"] = password_hash
        
        user = await self.user_repo.create(user_dict)
        return RegisterResponse.model_validate(user)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    async def create_access_token_for_user(self, user: User) -> str:
        """Generate JWT access token for user"""
        data = {
            "sub": str(user.id),
            "role": user.role.value
        }
        return create_access_token(data)
    
    async def create_refresh_token_for_user(self, user: User) -> str:
        """Generate JWT refresh token for user"""
        data = {
            "sub": str(user.id),
            "role": user.role.value
        }
        return create_refresh_token(data)
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Generate new access token from refresh token"""
        token_data = verify_token(refresh_token)
        if not token_data:
            return None
        
        user = await self.user_repo.get_by_id(token_data.user_id)
        if not user or not user.is_active:
            return None
        
        return await self.create_access_token_for_user(user)
    
    async def change_password(
        self,
        user_id: UUID,
        old_password: str,
        new_password: str
    ) -> bool:
        """Change user password"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        if not verify_password(old_password, user.password_hash):
            return False
        
        new_password_hash = hash_password(new_password)
        await self.user_repo.update(user_id, {"password_hash": new_password_hash})
        return True


