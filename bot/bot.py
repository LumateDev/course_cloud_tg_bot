import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import aiohttp

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Функция для получения данных о курсах с бэкенда
async def fetch_courses(endpoint: str):
    """Получение списка курсов с бэкенда."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/{endpoint}") as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"Ошибка при получении данных с бэкенда: {response.status}")
                return []


# Функции для клавиатур
def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура главного меню."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Доступные курсы", callback_data="available_courses")],
        [InlineKeyboardButton(text="Мои курсы", callback_data="my_courses")],
        [InlineKeyboardButton(text="Связаться с администратором", callback_data="contact_admin")]
    ])


def courses_keyboard(courses: list, back_callback: str) -> InlineKeyboardMarkup:
    """Клавиатура списка курсов."""
    buttons = [
        [InlineKeyboardButton(text=course["title"], callback_data=f"course_{course['id']}")]
        for course in courses
    ]
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=back_callback)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def course_management_keyboard(course_id: int) -> InlineKeyboardMarkup:
    """Клавиатура управления курсом."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Информация о курсе", callback_data=f"info_{course_id}")],
        [InlineKeyboardButton(text="Покинуть курс", callback_data=f"leave_{course_id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"course_{course_id}")]
    ])


def course_info_keyboard(course_id: int) -> InlineKeyboardMarkup:
    """Клавиатура только с кнопкой 'Назад' для раздела 'Информация о курсе'."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"course_{course_id}")]
    ])


# Обработчики команд
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer(
        text="Добро пожаловать! Я помогу вам управлять курсами.\n\n"
             "Вы можете:\n"
             "- Просматривать доступные курсы\n"
             "- Посмотреть ваши курсы\n"
             "- Записаться на курс\n"
             "- Покинуть курс",
        reply_markup=main_menu_keyboard()
    )


@dp.callback_query(lambda c: c.data == "available_courses")
async def show_available_courses(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Доступные курсы'."""
    available_courses = await fetch_courses("courses")
    await callback.message.edit_text(
        text="Доступные курсы:",
        reply_markup=courses_keyboard(available_courses, back_callback="main_menu")
    )


@dp.callback_query(lambda c: c.data == "my_courses")
async def show_my_courses(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Мои курсы'."""
    my_courses = await fetch_courses("courses")  # Здесь также используем правильный эндпоинт
    await callback.message.edit_text(
        text="Мои курсы:",
        reply_markup=courses_keyboard(my_courses, back_callback="main_menu")
    )


@dp.callback_query(lambda c: c.data.startswith("course_"))
async def manage_course(callback: CallbackQuery) -> None:
    """Обработчик выбора конкретного курса."""
    course_id = int(callback.data.split("_")[1])

    # Получаем информацию о выбранном курсе
    available_courses = await fetch_courses("courses")
    course = next((course for course in available_courses if course["id"] == course_id), None)

    if course:
        await callback.message.edit_text(
            text=f"Управление курсом {course['title']}:\nОписание: {course['description']}",
            reply_markup=course_management_keyboard(course_id)
        )
    else:
        await callback.message.answer("Этот курс не найден.")


@dp.callback_query(lambda c: c.data.startswith("info_"))
async def show_course_info(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Информация о курсе'."""
    course_id = int(callback.data.split("_")[1])
    available_courses = await fetch_courses("courses")
    course = next((course for course in available_courses if course["id"] == course_id), None)

    if course:
        await callback.message.edit_text(
            text=f"Информация о курсе {course['title']}:\nОписание: {course['description']}",
            reply_markup=course_info_keyboard(course_id)  # Используем клавиатуру с кнопкой "Назад"
        )
    else:
        await callback.message.answer("Информация о курсе не найдена.")


@dp.callback_query(lambda c: c.data.startswith("enroll_"))
async def enroll_course(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Записаться на курс'."""
    course_id = int(callback.data.split("_")[1])
    available_courses = await fetch_courses("courses")
    course = next((course for course in available_courses if course["id"] == course_id), None)

    if course:
        # Логика записи на курс, добавление в "Мои курсы"
        # Вместо этого здесь можно добавить курс в базу данных пользователя через API
        await callback.message.edit_text(
            text=f"Вы успешно записались на курс {course['title']}!",
            reply_markup=main_menu_keyboard()
        )
    else:
        await callback.message.answer("Не удалось записаться на курс.")


@dp.callback_query(lambda c: c.data.startswith("leave_"))
async def leave_course(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Покинуть курс'."""
    course_id = int(callback.data.split("_")[1])

    # Логика удаления курса из "Моих курсов"
    # Здесь можно удалить курс из базы данных пользователя через API
    await callback.message.edit_text(
        text=f"Вы покинули курс с ID {course_id}.",
        reply_markup=main_menu_keyboard()
    )


@dp.callback_query(lambda c: c.data == "contact_admin")
async def contact_admin(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Связаться с администратором'."""
    user_id = callback.from_user.id
    await bot.send_message(ADMIN_USER_ID,
                           f"Пользователь {callback.from_user.full_name} ({user_id}) хочет связаться с вами.")
    await callback.message.answer(
        "Ваше сообщение отправлено администратору. Он скоро свяжется с вами!"
    )


@dp.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Назад' в главное меню."""
    await callback.message.edit_text(
        text="Выберите действие:",
        reply_markup=main_menu_keyboard()
    )


# Главная функция
async def main() -> None:
    """Запуск бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
