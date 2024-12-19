from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, schemas
from backend.database import get_db

router = APIRouter()


# Получение курсов пользователя по Telegram ID
@router.get("/users/{telegram_id}/courses", response_model=List[schemas.CourseResponse])
async def get_courses_for_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    courses = await crud.get_courses_for_user(db, user.id)
    return courses


# Запись пользователя на курс
@router.post("/enroll", response_model=schemas.EnrollmentResponse)
async def enroll_user(enrollment_data: schemas.EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    existing_enrollment = await crud.get_enrollment_by_user_and_course(
        db, enrollment_data.user_id, enrollment_data.course_id
    )
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User already enrolled in this course")
    enrollment = await crud.enroll_user_on_course(db, enrollment_data.course_id, enrollment_data.user_id)
    return enrollment


# Удаление записи пользователя с курса
@router.delete("/leave_enrollment/{user_id}/{course_id}", response_model=schemas.EnrollmentResponse)
async def remove_enrollment(user_id: int, course_id: int, db: AsyncSession = Depends(get_db)):
    enrollment = await crud.get_enrollment_by_user_and_course(db, user_id, course_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment = await crud.remove_enrollment(db, enrollment.id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment could not be removed")
    return enrollment
