from aiogram import Router
from aiogram.types import CallbackQuery

from bot.keyboards.course_info import course_info_keyboard
from bot.keyboards.course_managment import course_management_keyboard
from bot.keyboards.main_menu import main_menu_keyboard
from bot.services.backend import fetch_courses
from bot.keyboards import course_info, course_managment

from bot.config import BACKEND_URL

courses_router = Router()

@courses_router.callback_query(lambda c: c.data == "available_courses")
async def show_available_courses(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Доступные курсы'."""
    available_courses = await fetch_courses("courses", BACKEND_URL)
    if not available_courses:
        await callback.message.edit_text(
            text="К сожалению, доступных курсов сейчас нет.",
            reply_markup=main_menu_keyboard()
        )
        return

    await callback.message.edit_text(
        text="Доступные курсы:",
        reply_markup=course_info_keyboard(available_courses, back_callback="main_menu")
    )


@courses_router.callback_query(lambda c: c.data.startswith("course_"))
async def manage_course(callback: CallbackQuery) -> None:
    """Обработчик выбора конкретного курса."""
    course_id = int(callback.data.split("_")[1])

    # Получаем информацию о выбранном курсе
    available_courses = await fetch_courses("courses", BACKEND_URL)
    course = next((course for course in available_courses if course["id"] == course_id), None)

    if course:
        await callback.message.edit_text(
            text=f"Управление курсом {course['title']}:\nОписание: {course['description']}",
            reply_markup=course_management_keyboard(course_id)
        )
    else:
        await callback.message.answer("Этот курс не найден.")
