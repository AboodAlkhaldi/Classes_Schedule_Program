from sqlalchemy import Column, String, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import InstructorTitle


class Instructor(BaseModel):
    __tablename__ = "instructors"
    
    full_name = Column(String(100), nullable=False)
    title = Column(ENUM(InstructorTitle), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    home_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    home_department = relationship("Department", back_populates="instructors")
    availability = relationship("InstructorAvailability", back_populates="instructor", cascade="all, delete-orphan")
    course_offerings = relationship("CourseOffering", back_populates="instructor")
    
    __table_args__ = (
        Index('idx_instructors_email', 'email'),
        Index('idx_instructors_home_dept', 'home_department_id'),
    )
    
    def __repr__(self):
        return f"<Instructor(id={self.id}, email={self.email}, title={self.title.value})>"

