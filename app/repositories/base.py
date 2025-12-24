from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.orm import selectinload

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create new record"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Get single record by ID"""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get single record by any field"""
        field_attr = getattr(self.model, field, None)
        if not field_attr:
            raise ValueError(f"Field {field} does not exist on {self.model.__name__}")
        
        result = await self.db.execute(
            select(self.model).where(field_attr == value)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """Get multiple records with filtering and pagination"""
        query = select(self.model)
        
        # Apply filters
        if filters:
            from app.utils.filters import build_dynamic_filters
            filter_list = build_dynamic_filters(self.model, filters)
            if filter_list:
                query = query.where(and_(*filter_list))
        
        # Apply ordering
        if order_by:
            if hasattr(self.model, order_by):
                column = getattr(self.model, order_by)
                query = query.order_by(column)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update(self, id: UUID, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Update existing record"""
        # Remove None values
        update_data = {k: v for k, v in obj_in.items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(id)
        
        await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await self.db.flush()
        return await self.get_by_id(id)
    
    async def delete(self, id: UUID) -> bool:
        """Delete record (hard delete)"""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.db.flush()
        return result.rowcount > 0
    
    async def soft_delete(self, id: UUID) -> bool:
        """Soft delete record (if model supports it)"""
        if not hasattr(self.model, 'is_deleted'):
            return await self.delete(id)
        
        await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(is_deleted=True)
        )
        await self.db.flush()
        return True
    
    async def exists(self, field: str, value: Any, exclude_id: Optional[UUID] = None) -> bool:
        """Check if record exists with given field value"""
        field_attr = getattr(self.model, field, None)
        if not field_attr:
            return False
        
        query = select(func.count()).select_from(self.model).where(field_attr == value)
        
        if exclude_id:
            query = query.where(self.model.id != exclude_id)
        
        result = await self.db.execute(query)
        count = result.scalar()
        return count > 0
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters"""
        query = select(func.count()).select_from(self.model)
        
        if filters:
            from app.utils.filters import build_dynamic_filters
            filter_list = build_dynamic_filters(self.model, filters)
            if filter_list:
                query = query.where(and_(*filter_list))
        
        result = await self.db.execute(query)
        return result.scalar() or 0

