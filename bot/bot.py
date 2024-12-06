from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.types import BotCommand
from bot.config import BOT_TOKEN
from bot.handlers.start import start_router  # Импортируем роутер старта
from bot.handlers.courses import courses_router  # Импортируем роутер курсов
from bot.handlers.admin import admin_router  # Импортируем роутер админов

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
# Инициализация диспетчера
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(start_router)
dp.include_router(courses_router)
dp.include_router(admin_router)

async def set_bot_commands():
    """Устанавливаем список команд для бота."""
    commands = [
        BotCommand(command="/start", description="Начать общение с ботом"),
    ]
    await bot.set_my_commands(commands)

async def main() -> None:
    """Запуск бота."""
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
