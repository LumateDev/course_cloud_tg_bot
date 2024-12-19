from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import UserCreate, UserResponse
from backend.crud import create_or_update_user, get_users, get_user_by_telegram_id
from backend.database import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Создаём нового пользователя или обновляем существующего."""
    return await create_or_update_user(db, user.telegram_id, user.name)


@router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    """Получаем список всех пользователей."""
    return await get_users(db)

@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram_id_endpoint(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Получить пользователя по его Telegram ID."""
    user = await get_user_by_telegram_id(db, telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user