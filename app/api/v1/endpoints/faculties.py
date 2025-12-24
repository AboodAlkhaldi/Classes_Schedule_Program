from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.faculty_service import FacultyService
from app.schemas.faculty.dto import FacultyCreate, FacultyUpdate
from app.schemas.faculty.response import FacultyResponse, FacultyListResponse
from app.dependencies import require_admin

router = APIRouter()


@router.get("/", response_model=FacultyListResponse)
async def list_faculties(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all faculties"""
    faculty_service = FacultyService(db)
    return await faculty_service.get_faculties(skip=skip, limit=limit)


@router.post("/", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    faculty_data: FacultyCreate,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Create new faculty (admin only)"""
    faculty_service = FacultyService(db)
    try:
        return await faculty_service.create_faculty(faculty_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get faculty by ID"""
    faculty_service = FacultyService(db)
    faculty = await faculty_service.get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    return faculty


@router.put("/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(
    faculty_id: UUID,
    faculty_data: FacultyUpdate,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Update faculty (admin only)"""
    faculty_service = FacultyService(db)
    faculty = await faculty_service.update_faculty(faculty_id, faculty_data)
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    faculty_id: UUID,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Delete faculty (admin only)"""
    faculty_service = FacultyService(db)
    success = await faculty_service.delete_faculty(faculty_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")

