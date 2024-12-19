from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Модели для курсов
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Модели для пользователей
class UserBase(BaseModel):
    telegram_id: int
    name: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime


# Модели для записей на курсы
class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    user: UserResponse
    course: CourseResponse
    enrolled_at: datetime


class EnrollmentRequest(BaseModel):
    user_id: int
    course_id: int


# Дополнительные схемы для улучшений
class UserWithCoursesResponse(UserResponse):
    courses: List[CourseResponse] = []


class CourseWithEnrollmentsResponse(CourseResponse):
    enrollments: List[EnrollmentResponse] = []
