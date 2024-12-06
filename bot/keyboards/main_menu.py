from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура главного меню."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Доступные курсы", callback_data="available_courses")],
        [InlineKeyboardButton(text="Связаться с администратором", callback_data="contact_admin")]
    ])
