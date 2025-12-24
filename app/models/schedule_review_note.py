import uuid
from sqlalchemy import Column, Text, ForeignKey, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
from app.core.constants import ReviewNoteType


class ScheduleReviewNote(Base):
    """ScheduleReviewNote model without updated_at timestamp"""
    __tablename__ = "schedule_review_notes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    note_type = Column(ENUM(ReviewNoteType), nullable=False)
    message = Column(Text, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    schedule = relationship("Schedule", back_populates="review_notes")
    created_by_user = relationship("User", back_populates="review_notes")
    
    __table_args__ = (
        Index('idx_review_notes_schedule', 'schedule_id'),
    )
    
    def __repr__(self):
        return f"<ScheduleReviewNote(id={self.id}, note_type={self.note_type.value})>"

