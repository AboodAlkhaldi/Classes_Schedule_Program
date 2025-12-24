from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import ScheduleStatus


class Schedule(BaseModel):
    __tablename__ = "schedules"
    
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(ENUM(ScheduleStatus), default=ScheduleStatus.DRAFT, nullable=False, index=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    evaluated_at = Column(DateTime(timezone=True), nullable=True)
    evaluated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    term = relationship("Term", back_populates="schedules")
    department = relationship("Department", back_populates="schedules")
    submitter = relationship("User", foreign_keys=[submitted_by], back_populates="submitted_schedules")
    evaluator = relationship("User", foreign_keys=[evaluated_by], back_populates="evaluated_schedules")
    assignments = relationship("ScheduleAssignment", back_populates="schedule", cascade="all, delete-orphan")
    review_notes = relationship("ScheduleReviewNote", back_populates="schedule", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_schedules_term_dept', 'term_id', 'department_id'),
        Index('idx_schedules_status', 'status'),
    )
    
    def __repr__(self):
        return f"<Schedule(id={self.id}, status={self.status.value}, term_id={self.term_id})>"

