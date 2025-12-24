from sqlalchemy import Column, String, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Faculty(BaseModel):
    __tablename__ = "faculties"
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True)
    
    # Relationships
    departments = relationship("Department", back_populates="faculty", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_faculties_code', 'code'),
    )
    
    def __repr__(self):
        return f"<Faculty(id={self.id}, code={self.code}, name={self.name})>"

