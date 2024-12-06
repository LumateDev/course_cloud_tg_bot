from aiogram import types
from aiogram import Router
from aiogram.types import Message
from bot.keyboards.main_menu import main_menu_keyboard

start_router = Router()

@start_router.message(commands=['start'])
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer(
        text="Добро пожаловать! Я помогу вам управлять курсами.\n\n"
             "Вы можете:\n"
             "- Просматривать доступные курсы\n"
             "- Записаться на курс\n"
             "- Связаться с администратором",
        reply_markup=main_menu_keyboard()
    )
