from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ScheduleAssignment(BaseModel):
    __tablename__ = "schedule_assignments"
    
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    course_offering_id = Column(UUID(as_uuid=True), ForeignKey("course_offerings.id", ondelete="CASCADE"), nullable=False)
    time_slot_id = Column(UUID(as_uuid=True), ForeignKey("time_slots.id", ondelete="CASCADE"), nullable=False)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey("classrooms.id", ondelete="RESTRICT"), nullable=False)
    
    # Relationships
    schedule = relationship("Schedule", back_populates="assignments")
    course_offering = relationship("CourseOffering", back_populates="schedule_assignments")
    time_slot = relationship("TimeSlot", back_populates="schedule_assignments")
    classroom = relationship("Classroom", back_populates="schedule_assignments")
    
    __table_args__ = (
        UniqueConstraint('schedule_id', 'course_offering_id', 'time_slot_id', name='uq_schedule_assignment'),
        Index('idx_schedule_assignments_composite', 'schedule_id', 'time_slot_id', 'classroom_id'),
    )
    
    def __repr__(self):
        return f"<ScheduleAssignment(id={self.id}, schedule_id={self.schedule_id})>"

