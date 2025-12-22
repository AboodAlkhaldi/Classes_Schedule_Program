from collections.abc import AsyncGenerator
import uuid 

from sqlalchemy import Column, String , Text , DateTime , ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine , async_sessionmaker
from sqlalchemy.orm import DeclarativeBase , relationship
from datetime import datetime
import os



DATABASE_URL = os.getenv("DATABASE_URL")

# just dummy table initialization for testing purposes 

class BlaBla(DeclarativeBase):
    __tablename__ = "blablas"

    id = Column(UUID(as_uuid=True) , primary_key=True , default=uuid.uuid4)
    caption = Column(Text)
    url= Column(String(255) , nullable=False)
    created_at = Column(DateTime , default=datetime.now)
 
 
 # end for dummy tables 


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine , expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)

async def get_async_session() -> AsyncGenerator(AsyncSession , None):
    async with async_session_maker() as session:
        yield session


