from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Course, User, Enrollment
from schemas import CourseCreate, UserCreate, EnrollmentCreate

# CRUD для курсов
async def create_course(db: AsyncSession, course: CourseCreate):
    new_course = Course(**course.dict())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


async def get_courses(db: AsyncSession):
    result = await db.execute(select(Course))
    return result.scalars().all()


# CRUD для пользователей
async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


# CRUD для записей на курсы
async def create_enrollment(db: AsyncSession, enrollment: EnrollmentCreate):
    new_enrollment = Enrollment(**enrollment.dict())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    return new_enrollment


async def get_enrollments(db: AsyncSession):
    result = await db.execute(select(Enrollment).options(
        select(User), select(Course)
    ))
    return result.scalars().all()
