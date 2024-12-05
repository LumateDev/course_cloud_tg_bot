from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import CourseCreate, CourseResponse
from backend.crud import create_course, get_courses
from backend.database import get_db

router = APIRouter()

@router.post("/", response_model=CourseResponse)
async def create_new_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await create_course(db, course)

@router.get("/", response_model=list[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db)):
    return await get_courses(db)
