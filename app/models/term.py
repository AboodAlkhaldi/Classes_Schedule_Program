from sqlalchemy import Column, String, Date, Boolean, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy import func, extract
from app.models.base import BaseModel


class Term(BaseModel):
    __tablename__ = "terms"
    
    name = Column(String(50), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    courses = relationship("Course", back_populates="term")
    course_offerings = relationship("CourseOffering", back_populates="term")
    time_slots = relationship("TimeSlot", back_populates="term", cascade="all, delete-orphan")
    instructor_availability = relationship("InstructorAvailability", back_populates="term", cascade="all, delete-orphan")
    program_classes = relationship("ProgramClass", back_populates="term", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="term")
    
    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_term_date_range'),
        Index('idx_terms_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<Term(id={self.id}, name={self.name}, is_active={self.is_active})>"

