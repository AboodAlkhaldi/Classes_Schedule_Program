from typing import List, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from app.models.term import Term
from app.repositories.base import BaseRepository


class TermRepository(BaseRepository[Term]):
    def __init__(self, db: AsyncSession):
        super().__init__(Term, db)
    
    async def get_active_term(self) -> Optional[Term]:
        """Get currently active term"""
        result = await self.db.execute(
            select(Term).where(Term.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> Optional[Term]:
        """Get term by name"""
        return await self.get_by_field("name", name)
    
    async def check_overlapping_terms(
        self,
        start_date: date,
        end_date: date,
        exclude_id: Optional[UUID] = None
    ) -> bool:
        """Check if date range overlaps with existing terms"""
        query = select(Term).where(
            and_(
                Term.start_date <= end_date,
                Term.end_date >= start_date
            )
        )
        
        if exclude_id:
            query = query.where(Term.id != exclude_id)
        
        result = await self.db.execute(query)
        overlapping = result.scalar_one_or_none()
        return overlapping is not None
    
    async def activate_term(self, term_id: UUID) -> Optional[Term]:
        """Set term as active and deactivate others"""
        # Deactivate all terms
        await self.db.execute(
            select(Term).where(Term.is_active == True)
        )
        
        # Activate the specified term
        term = await self.update(term_id, {"is_active": True})
        await self.db.commit()
        return term

