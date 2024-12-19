# backend/main.py
from fastapi import FastAPI
from backend.routers import courses, users, enrollments  # Подключаем роутеры
from backend.database import engine, Base  # Настройки базы данных

# Создаем приложение FastAPI
app = FastAPI()

# Регистрируем роутеры с уникальными префиксами
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])

# Создание таблиц в базе данных при старте
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Тестовый эндпоинт
@app.get("/")
async def root():
    return {"message": "API is running!"}
