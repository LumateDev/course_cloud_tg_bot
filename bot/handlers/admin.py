from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.bot import bot
from bot.config import ADMIN_USER_ID
from bot.states.user_states import Form

admin_router = Router()


@admin_router.callback_query(lambda c: c.data == "contact_admin")
async def contact_admin(callback: CallbackQuery, state: FSMContext) -> None:
    user_name = callback.from_user.username or "Неизвестный пользователь"
    await callback.answer()
    # Запросить у пользователя сообщение
    await callback.message.answer("Напишите ваше сообщение для администратора.")
    await state.set_state(Form.waiting_for_message)  # Переводим пользователя в состояние ожидания сообщения


@admin_router.message(state=Form.waiting_for_message)
async def handle_message(message: Message, state: FSMContext):
    user_name = message.from_user.username or "Неизвестный пользователь"
    user_message = message.text

    # Отправить сообщение админу
    await bot.send_message(ADMIN_USER_ID, f"Сообщение от {user_name}:\n{user_message}")

    # Ответить пользователю
    await message.answer("Ваше сообщение отправлено администратору.")

    # Очистить состояние
    await state.clear()
