from fastapi import FastAPI , HTTPException , Depends
from app.db import BlaBla, create_db_and_tables , get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/hello")
def hello():
    if not True:
        raise HTTPException(status_code=404 , detail="Not found")   
    

    return {"message" : "Hello lan"} 

