from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Шаблон для создания/обновления курса
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


# Шаблон для создания пользователя
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Шаблоны для записи на курс
class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_at: datetime
    user: UserResponse
    course: CourseResponse

    class Config:
        orm_mode = True
