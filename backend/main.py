from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT 1")
    return {"success": True, "result": result.scalar()}
