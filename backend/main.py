# backend/main.py
from fastapi import FastAPI
from backend.routers import courses, users, enrollments  # Подключаем роутеры

# Создаем приложение FastAPI
app = FastAPI()

# Регистрируем роутеры с уникальными префиксами
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])


# Тестовый эндпоинт
@app.get("/")
async def root():
    return {"message": "API is running!"}
