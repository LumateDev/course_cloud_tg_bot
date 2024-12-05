from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Создаем базовый класс для моделей
Base = declarative_base()

# Создание асинхронного движка для работы с PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Создаем сессию AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Асинхронная зависимость для получения сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session  # Возвращаем сессию для использования в запросах
