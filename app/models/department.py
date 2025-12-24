from sqlalchemy import Column, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"
    
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculties.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String(3), nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="departments")
    users = relationship("User", back_populates="department")
    instructors = relationship("Instructor", back_populates="home_department")
    courses = relationship("Course", back_populates="department")
    classrooms = relationship("Classroom", back_populates="department")
    program_classes = relationship("ProgramClass", back_populates="department")
    schedules = relationship("Schedule", back_populates="department")
    
    __table_args__ = (
        UniqueConstraint('faculty_id', 'code', name='uq_department_faculty_code'),
        Index('idx_departments_faculty', 'faculty_id'),
    )
    
    def __repr__(self):
        return f"<Department(id={self.id}, code={self.code}, name={self.name})>"

