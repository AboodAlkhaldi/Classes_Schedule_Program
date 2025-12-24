from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, faculties, schedules

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(faculties.router, prefix="/faculties", tags=["faculties"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])

