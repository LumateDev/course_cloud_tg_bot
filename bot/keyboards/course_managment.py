from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def course_management_keyboard(course_id: int) -> InlineKeyboardMarkup:
    """Клавиатура управления курсом."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Информация о курсе", callback_data=f"info_{course_id}")],
        [InlineKeyboardButton(text="Записаться на курс", callback_data=f"enroll_{course_id}")],
        [InlineKeyboardButton(text="Назад", callback_data="available_courses")]
    ])
