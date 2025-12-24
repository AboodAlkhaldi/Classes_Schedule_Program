from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.faculty import FacultyRepository
from app.schemas.faculty.dto import FacultyCreate, FacultyUpdate
from app.schemas.faculty.response import FacultyResponse, FacultyListResponse
from app.utils.normalization import normalize_faculty_code
from app.utils.validators import validate_faculty_code


class FacultyService:
    def __init__(self, db: AsyncSession):
        self.faculty_repo = FacultyRepository(db)
        self.db = db
    
    async def create_faculty(self, faculty_data: FacultyCreate) -> FacultyResponse:
        """Create new faculty"""
        # Normalize code
        code = normalize_faculty_code(faculty_data.code)
        
        # Validate code
        if not validate_faculty_code(code):
            raise ValueError("Faculty code must be exactly 3 uppercase letters")
        
        # Check if code exists
        existing = await self.faculty_repo.get_by_code(code)
        if existing:
            raise ValueError("Faculty with this code already exists")
        
        # Create faculty
        faculty_dict = faculty_data.model_dump()
        faculty_dict["code"] = code
        faculty = await self.faculty_repo.create(faculty_dict)
        return FacultyResponse.model_validate(faculty)
    
    async def get_faculty(self, faculty_id: UUID) -> Optional[FacultyResponse]:
        """Get faculty by ID"""
        faculty = await self.faculty_repo.get_by_id(faculty_id)
        if not faculty:
            return None
        return FacultyResponse.model_validate(faculty)
    
    async def get_faculties(
        self,
        skip: int = 0,
        limit: int = 50
    ) -> FacultyListResponse:
        """Get list of faculties"""
        faculties = await self.faculty_repo.get_multi(skip=skip, limit=limit)
        total = await self.faculty_repo.count()
        
        return FacultyListResponse(
            items=[FacultyResponse.model_validate(f) for f in faculties],
            total=total,
            page=(skip // limit) + 1,
            page_size=limit
        )
    
    async def update_faculty(
        self,
        faculty_id: UUID,
        faculty_data: FacultyUpdate
    ) -> Optional[FacultyResponse]:
        """Update faculty"""
        update_dict = faculty_data.model_dump(exclude_unset=True)
        
        # Normalize code if provided
        if "code" in update_dict and update_dict["code"]:
            update_dict["code"] = normalize_faculty_code(update_dict["code"])
        
        faculty = await self.faculty_repo.update(faculty_id, update_dict)
        if not faculty:
            return None
        return FacultyResponse.model_validate(faculty)
    
    async def delete_faculty(self, faculty_id: UUID) -> bool:
        """Delete faculty"""
        return await self.faculty_repo.delete(faculty_id)


