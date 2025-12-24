from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import ClassroomType


class Classroom(BaseModel):
    __tablename__ = "classrooms"
    
    code = Column(String(20), unique=True, nullable=False)
    classroom_type = Column(ENUM(ClassroomType), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    capacity = Column(Integer, nullable=False)
    features = Column(JSONB, default={}, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    department = relationship("Department", back_populates="classrooms")
    course_offerings = relationship("CourseOffering", back_populates="classroom")
    schedule_assignments = relationship("ScheduleAssignment", back_populates="classroom")
    
    __table_args__ = (
        CheckConstraint('capacity BETWEEN 1 AND 300', name='check_capacity'),
        Index('idx_classrooms_department', 'department_id'),
    )
    
    def __repr__(self):
        return f"<Classroom(id={self.id}, code={self.code}, capacity={self.capacity})>"

