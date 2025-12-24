from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.schedule_service import ScheduleService
from app.schemas.schedule.dto import ScheduleCreate, ScheduleSubmit, ScheduleApproval
from app.schemas.schedule.response import ScheduleResponse, ScheduleDetailResponse
from app.schemas.schedule.assignment import ScheduleAssignmentCreate, ScheduleAssignmentResponse
from app.dependencies import get_current_user, require_dean
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new schedule"""
    schedule_service = ScheduleService(db)
    try:
        return await schedule_service.create_schedule(schedule_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{schedule_id}", response_model=ScheduleDetailResponse)
async def get_schedule(
    schedule_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get schedule details"""
    schedule_service = ScheduleService(db)
    schedule = await schedule_service.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return schedule


@router.post("/{schedule_id}/assignments", response_model=ScheduleAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def add_assignment(
    schedule_id: UUID,
    assignment_data: ScheduleAssignmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add assignment to schedule"""
    schedule_service = ScheduleService(db)
    try:
        return await schedule_service.add_assignment(schedule_id, assignment_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{schedule_id}/submit", response_model=ScheduleResponse)
async def submit_schedule(
    schedule_id: UUID,
    submit_data: ScheduleSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit schedule for approval"""
    schedule_service = ScheduleService(db)
    try:
        return await schedule_service.submit_for_approval(schedule_id, current_user.id, submit_data.notes)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{schedule_id}/approve", response_model=ScheduleResponse)
async def approve_schedule(
    schedule_id: UUID,
    approval_data: ScheduleApproval,
    current_user: User = Depends(require_dean),
    db: AsyncSession = Depends(get_db)
):
    """Approve schedule (dean/admin only)"""
    schedule_service = ScheduleService(db)
    if approval_data.approved:
        try:
            return await schedule_service.approve_schedule(schedule_id, current_user.id, approval_data.notes)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        try:
            return await schedule_service.reject_schedule(schedule_id, current_user.id, approval_data.notes)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

