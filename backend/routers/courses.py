from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import CourseCreate, CourseResponse
from backend.crud import create_course, get_courses, get_course_by_id

router = APIRouter()

@router.post("/", response_model=CourseResponse)
async def create_new_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await create_course(db, course)

@router.get("/", response_model=list[CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db)):
    return await get_courses(db)


# Получение курса по ID
@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    """Получить курс по ID."""
    course = await get_course_by_id(db, course_id)  # Вызовем функцию, которая получит курс по ID

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course



