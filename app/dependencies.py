from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.core.security import verify_token
from app.repositories.user import UserRepository
from app.models.user import User
from app.core.constants import UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(token_data.user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(allowed_roles: List[str]):
    """Dependency to check user role"""
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(allowed_roles)}"
            )
        return current_user
    
    return role_checker


# Role-specific dependencies
async def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_dean(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.DEAN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dean or Admin access required"
        )
    return current_user


async def require_dept_rep(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.DEAN, UserRole.DEPARTMENT_REP]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Department Representative, Dean, or Admin access required"
        )
    return current_user

