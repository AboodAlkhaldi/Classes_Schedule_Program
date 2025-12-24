from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user.response import UserResponse
from app.services.auth_service import AuthService
from app.schemas.auth.login import LoginRequest, LoginResponse
from app.schemas.user.dto import PasswordReset, UserCreate
from app.dependencies import get_current_user
from app.models.user import User 
from app.schemas.auth.register import RegisterRequest , RegisterResponse


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login user"""
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = await auth_service.create_access_token_for_user(user)
    refresh_token = await auth_service.create_refresh_token_for_user(user)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """register user"""
    auth_service = AuthService(db)
    user = await auth_service.register_user(register_data)
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    access_token = await auth_service.create_access_token_for_user(user)
    refresh_token = await auth_service.create_refresh_token_for_user(user)

    return RegisterResponse(
        email=user.email,
        id=user.id,
        name=user.name,
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token"""
    auth_service = AuthService(db)
    access_token = await auth_service.refresh_access_token(refresh_token)
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/change-password")
async def change_password(
    password_data: PasswordReset,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    auth_service = AuthService(db)
    success = await auth_service.change_password(
        current_user.id,
        password_data.old_password,
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid old password"
        )
    
    return {"message": "Password changed successfully"}

