import uuid
from sqlalchemy import Column, Time, ForeignKey, UniqueConstraint, CheckConstraint, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from app.core.constants import DayOfWeek


class TimeSlot(Base):
    """TimeSlot model without updated_at timestamp"""
    __tablename__ = "time_slots"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(ENUM(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    term = relationship("Term", back_populates="time_slots")
    instructor_availability = relationship("InstructorAvailability", back_populates="time_slot")
    schedule_assignments = relationship("ScheduleAssignment", back_populates="time_slot")
    
    __table_args__ = (
        UniqueConstraint('term_id', 'day_of_week', 'start_time', name='uq_time_slot'),
        Index('idx_time_slots_term_day', 'term_id', 'day_of_week'),
    )
    
    def __repr__(self):
        return f"<TimeSlot(id={self.id}, day={self.day_of_week.value}, start={self.start_time})>"

