from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import CourseLevel, CourseType


class Course(BaseModel):
    __tablename__ = "courses"
    
    code = Column(String(6), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True)
    class_level = Column(ENUM(CourseLevel), nullable=False)
    weekly_hours = Column(Integer, nullable=False)
    course_type = Column(ENUM(CourseType), nullable=False)
    parent_course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    is_retake_critical = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    department = relationship("Department", back_populates="courses")
    term = relationship("Term", back_populates="courses")
    parent_course = relationship("Course", remote_side=[BaseModel.id], backref="child_courses")
    offerings = relationship("CourseOffering", back_populates="course", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('code', 'term_id', name='uq_course_code_term'),
        CheckConstraint('weekly_hours IN (1,2,3,4,5,6,7,8,9)', name='check_weekly_hours'),
        Index('idx_courses_code', 'code'),
        Index('idx_courses_term', 'term_id'),
    )
    
    def __repr__(self):
        return f"<Course(id={self.id}, code={self.code}, name={self.name})>"

