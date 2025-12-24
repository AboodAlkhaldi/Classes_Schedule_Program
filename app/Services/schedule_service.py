from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.schedule import ScheduleRepository
from app.repositories.schedule_assignment import ScheduleAssignmentRepository
from app.schemas.schedule.dto import ScheduleCreate, ScheduleSubmit, ScheduleApproval
from app.schemas.schedule.response import ScheduleResponse, ScheduleDetailResponse
from app.schemas.schedule.assignment import ScheduleAssignmentCreate, ScheduleAssignmentResponse
from app.core.constants import ScheduleStatus


class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.schedule_repo = ScheduleRepository(db)
        self.assignment_repo = ScheduleAssignmentRepository(db)
        self.db = db
    
    async def create_schedule(
        self,
        schedule_data: ScheduleCreate,
        user_id: UUID
    ) -> ScheduleResponse:
        """Create new schedule for term/department"""
        # Check if schedule already exists
        existing = await self.schedule_repo.get_by_term_and_department(
            schedule_data.term_id,
            schedule_data.department_id
        )
        if existing:
            raise ValueError("Schedule already exists for this term and department")
        
        schedule_dict = schedule_data.model_dump()
        schedule_dict["submitted_by"] = user_id
        schedule_dict["status"] = ScheduleStatus.DRAFT
        
        schedule = await self.schedule_repo.create(schedule_dict)
        return ScheduleResponse.model_validate(schedule)
    
    async def get_schedule(self, schedule_id: UUID) -> Optional[ScheduleDetailResponse]:
        """Get schedule with all details"""
        schedule = await self.schedule_repo.get_by_id(schedule_id)
        if not schedule:
            return None
        
        assignments = await self.assignment_repo.get_by_schedule(schedule_id)
        
        schedule_dict = ScheduleResponse.model_validate(schedule).model_dump()
        schedule_dict["assignments"] = [
            ScheduleAssignmentResponse.model_validate(a).model_dump()
            for a in assignments
        ]
        schedule_dict["review_notes"] = []  # Can be populated from review_notes relationship
        
        return ScheduleDetailResponse(**schedule_dict)
    
    async def add_assignment(
        self,
        schedule_id: UUID,
        assignment_data: ScheduleAssignmentCreate,
        user_id: UUID
    ) -> ScheduleAssignmentResponse:
        """Add course assignment to schedule"""
        # Check for conflicts
        from app.repositories.course_offering import CourseOfferingRepository
        course_offering_repo = CourseOfferingRepository(self.db)
        course_offering = await course_offering_repo.get_by_id(assignment_data.course_offering_id)
        
        if not course_offering:
            raise ValueError("Course offering not found")
        
        # Check instructor conflict
        has_conflict = await self.assignment_repo.check_instructor_conflict(
            course_offering.instructor_id,
            assignment_data.time_slot_id,
            schedule_id
        )
        if has_conflict:
            raise ValueError("Instructor conflict detected")
        
        # Check classroom conflict
        has_conflict = await self.assignment_repo.check_classroom_conflict(
            assignment_data.classroom_id,
            assignment_data.time_slot_id,
            schedule_id
        )
        if has_conflict:
            raise ValueError("Classroom conflict detected")
        
        assignment_dict = assignment_data.model_dump()
        assignment_dict["schedule_id"] = schedule_id
        
        assignment = await self.assignment_repo.create(assignment_dict)
        return ScheduleAssignmentResponse.model_validate(assignment)
    
    async def submit_for_approval(
        self,
        schedule_id: UUID,
        user_id: UUID,
        notes: Optional[str] = None
    ) -> ScheduleResponse:
        """Submit schedule for approval"""
        schedule = await self.schedule_repo.submit_schedule(schedule_id, user_id)
        if not schedule:
            raise ValueError("Schedule not found")
        return ScheduleResponse.model_validate(schedule)
    
    async def approve_schedule(
        self,
        schedule_id: UUID,
        user_id: UUID,
        notes: str
    ) -> ScheduleResponse:
        """Approve schedule (dean/admin only)"""
        schedule = await self.schedule_repo.approve_schedule(schedule_id, user_id)
        if not schedule:
            raise ValueError("Schedule not found")
        return ScheduleResponse.model_validate(schedule)
    
    async def reject_schedule(
        self,
        schedule_id: UUID,
        user_id: UUID,
        reason: str
    ) -> ScheduleResponse:
        """Reject schedule with reason"""
        schedule = await self.schedule_repo.reject_schedule(schedule_id, user_id)
        if not schedule:
            raise ValueError("Schedule not found")
        return ScheduleResponse.model_validate(schedule)


