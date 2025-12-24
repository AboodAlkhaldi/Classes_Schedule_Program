from sqlalchemy import Column, String, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import UserRole


class User(BaseModel):
    __tablename__ = "users"
    
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(ENUM(UserRole), nullable=False, index=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relationships
    department = relationship("Department", back_populates="users")
    submitted_schedules = relationship("Schedule", foreign_keys="Schedule.submitted_by", back_populates="submitter")
    evaluated_schedules = relationship("Schedule", foreign_keys="Schedule.evaluated_by", back_populates="evaluator")
    instructor_availability_created = relationship("InstructorAvailability", back_populates="created_by_user")
    review_notes = relationship("ScheduleReviewNote", back_populates="created_by_user")
    
    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_department', 'department_id'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"

