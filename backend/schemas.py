from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    user: UserResponse
    course: CourseResponse
    enrolled_at: datetime

    class Config:
        orm_mode = True
