from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import UserCreate, UserResponse
from backend.crud import create_user, get_users
from backend.database import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)
