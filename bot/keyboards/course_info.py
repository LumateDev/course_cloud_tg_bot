from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def course_info_keyboard(course_id: int) -> InlineKeyboardMarkup:
    """Клавиатура только с кнопкой 'Назад' для раздела 'Информация о курсе'."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"course_{course_id}")]
    ])
