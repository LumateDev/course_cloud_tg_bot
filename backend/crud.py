from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from backend import models
from backend.models import Course, User, Enrollment
from backend.schemas import CourseCreate, UserCreate, EnrollmentCreate


# CRUD для пользователей
async def create_or_update_user(db: AsyncSession, telegram_id: int, name: str):
    """Создать или обновить пользователя по Telegram ID."""
    result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(telegram_id=telegram_id, name=name)
        db.add(user)
    else:
        if user.name != name:
            user.name = name

    try:
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении пользователя: {str(e)}")

    return user


async def get_users(db: AsyncSession):
    """Получить всех пользователей."""
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int):
    """Получить пользователя по его Telegram ID."""
    result = await db.execute(select(User).filter(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


# Функция для получения всех курсов
async def get_courses(db: AsyncSession):
    """Получить все курсы."""
    result = await db.execute(select(Course))
    return result.scalars().all()


async def get_course_by_id(db: AsyncSession, course_id: int):
    """Получить курс по ID."""
    result = await db.execute(select(Course).filter(Course.id == course_id))
    return result.scalar_one_or_none()


# Функция для создания курса
async def create_course(db: AsyncSession, course: CourseCreate):
    """Создать новый курс."""
    new_course = Course(**course.dict())
    db.add(new_course)

    try:
        await db.commit()
        await db.refresh(new_course)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании курса: {str(e)}")

    return new_course


# Дополнительная функция для проверки, записан ли пользователь на курс
async def get_enrollments_for_user_and_course(db: AsyncSession, user_id: int, course_id: int):
    """Проверить, записан ли пользователь на курс."""
    result = await db.execute(
        select(Enrollment).filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
    )
    return result.scalar_one_or_none()


# CRUD для записей на курсы
async def create_enrollment(db: AsyncSession, enrollment: EnrollmentCreate):
    """Создать новую запись на курс."""
    # Проверяем, существует ли уже запись
    existing_enrollment = await get_enrollments_for_user_and_course(db, enrollment.user_id, enrollment.course_id)
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User is already enrolled in this course")

    # Создаем новую запись
    new_enrollment = Enrollment(user_id=enrollment.user_id, course_id=enrollment.course_id)
    db.add(new_enrollment)

    try:
        await db.commit()
        await db.refresh(new_enrollment)
        return new_enrollment
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при записи на курс: {str(e)}")


# Функция для получения курсов для пользователя
async def get_courses_for_user(db: AsyncSession, user_id: int):
    """Получить все курсы, на которые записан пользователь."""
    result = await db.execute(
        select(Course).join(Enrollment).filter(Enrollment.user_id == user_id)
    )
    return result.scalars().all()


# Функция для записи пользователя на курс
async def enroll_user_on_course(db: AsyncSession, course_id: int, user_id: int):
    """Записать пользователя на курс."""
    existing_enrollment = await get_enrollments_for_user_and_course(db, user_id, course_id)
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User is already enrolled in this course")

    # Создание новой записи на курс
    new_enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(new_enrollment)

    try:
        await db.commit()
        await db.refresh(new_enrollment)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при записи на курс: {str(e)}")

    return new_enrollment


async def get_enrollment_by_user_and_course(db: AsyncSession, user_id: int, course_id: int):
    result = await db.execute(
        select(models.Enrollment).filter(models.Enrollment.user_id == user_id, models.Enrollment.course_id == course_id)
    )
    enrollment = result.scalars().first()
    return enrollment


# Функция для удаления записи
async def remove_enrollment(db: AsyncSession, enrollment_id: int):
    print(f"Attempting to delete enrollment with ID: {enrollment_id}")
    stmt = select(Enrollment).filter(Enrollment.id == enrollment_id)
    result = await db.execute(stmt)
    enrollment = result.scalars().first()
    if not enrollment:
        print(f"No enrollment found with ID {enrollment_id}")
        return None
    print(f"Found enrollment: {enrollment}")
    await db.delete(enrollment)
    await db.commit()
    print(f"Deleted enrollment: {enrollment}")
    return enrollment
