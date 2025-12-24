import uuid
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import Column, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base declarative class for all models"""
    pass


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps"""
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class IDMixin:
    """Mixin to add UUID primary key"""
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )


class SoftDeleteMixin:
    """Mixin to add soft delete functionality"""
    
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    def soft_delete(self):
        """Mark record as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    def restore(self):
        """Restore soft-deleted record"""
        self.is_deleted = False
        self.deleted_at = None


class BaseModel(Base, IDMixin, TimestampMixin):
    """Base model with ID and timestamps"""
    __abstract__ = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create model instance from dictionary"""
        return cls(**data)

