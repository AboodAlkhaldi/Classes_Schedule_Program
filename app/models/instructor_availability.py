import uuid
from sqlalchemy import Column, Boolean, ForeignKey, UniqueConstraint, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class InstructorAvailability(Base):
    """InstructorAvailability model without updated_at timestamp"""
    __tablename__ = "instructor_availability"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False, index=True)
    time_slot_id = Column(UUID(as_uuid=True), ForeignKey("time_slots.id", ondelete="CASCADE"), nullable=False, index=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    term = relationship("Term", back_populates="instructor_availability")
    instructor = relationship("Instructor", back_populates="availability")
    time_slot = relationship("TimeSlot", back_populates="instructor_availability")
    created_by_user = relationship("User", back_populates="instructor_availability_created")
    
    __table_args__ = (
        UniqueConstraint('term_id', 'instructor_id', 'time_slot_id', name='uq_instructor_availability'),
        Index('idx_instructor_avail_composite', 'term_id', 'instructor_id', 'time_slot_id'),
    )
    
    def __repr__(self):
        return f"<InstructorAvailability(id={self.id}, instructor_id={self.instructor_id}, is_available={self.is_available})>"

