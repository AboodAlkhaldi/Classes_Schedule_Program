from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.constants import ClassLevel, ClassLabel


class ProgramClass(BaseModel):
    __tablename__ = "program_classes"
    
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True)
    class_level = Column(ENUM(ClassLevel), nullable=False)
    group_no = Column(Integer, nullable=False)
    label = Column(ENUM(ClassLabel), nullable=False)
    
    # Relationships
    department = relationship("Department", back_populates="program_classes")
    term = relationship("Term", back_populates="program_classes")
    
    __table_args__ = (
        UniqueConstraint('department_id', 'term_id', 'class_level', 'group_no', name='uq_program_class'),
    )
    
    def __repr__(self):
        return f"<ProgramClass(id={self.id}, class_level={self.class_level.value}, group_no={self.group_no})>"

