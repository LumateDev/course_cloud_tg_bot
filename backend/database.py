from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings
from ssl import create_default_context

# Создаем базовый класс для моделей
Base = declarative_base()

ctx = create_default_context(
    cafile=settings.SSL_CERT_PATH
)


# Создание асинхронного движка для работы с PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, connect_args={"ssl": ctx}, echo=True)

# Создаем сессию AsyncSession
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# Асинхронная зависимость для получения сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session  # Возвращаем сессию для использования в запросах
