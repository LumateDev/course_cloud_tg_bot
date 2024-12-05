from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import EnrollmentCreate, EnrollmentResponse
from backend.crud import create_enrollment, get_enrollments
from backend.database import get_db

router = APIRouter()

@router.post("/", response_model=EnrollmentResponse)
async def enroll_user(enrollment: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    return await create_enrollment(db, enrollment)

@router.get("/", response_model=list[EnrollmentResponse])
async def list_enrollments(db: AsyncSession = Depends(get_db)):
    return await get_enrollments(db)
