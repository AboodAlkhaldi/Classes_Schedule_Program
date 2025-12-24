from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class CourseOffering(BaseModel):
    __tablename__ = "course_offerings"
    
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id", ondelete="RESTRICT"), nullable=False, index=True)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="RESTRICT"), nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True)
    group_no = Column(Integer, nullable=True)
    student_count = Column(Integer, nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="offerings")
    instructor = relationship("Instructor", back_populates="course_offerings")
    classroom = relationship("Classroom", back_populates="course_offerings")
    term = relationship("Term", back_populates="course_offerings")
    schedule_assignments = relationship("ScheduleAssignment", back_populates="course_offering")
    
    __table_args__ = (
        UniqueConstraint('course_id', 'term_id', 'group_no', name='uq_course_offering'),
        CheckConstraint('student_count BETWEEN 1 AND 300', name='check_student_count'),
        Index('idx_course_offerings_composite', 'course_id', 'term_id', 'instructor_id'),
    )
    
    def __repr__(self):
        return f"<CourseOffering(id={self.id}, course_id={self.course_id}, instructor_id={self.instructor_id})>"

