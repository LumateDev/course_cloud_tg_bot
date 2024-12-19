import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session import aiohttp
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMIN_USER_ID
from services import fetch_courses, get_course_by_id, get_user_by_telegram_id, create_or_update_user, \
    fetch_user_courses, create_enrollment, check_existing_enrollment, remove_enrollment

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Основное меню
def main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    """Главное меню с опцией для администратора."""
    buttons = [
        [InlineKeyboardButton(text="Доступные курсы", callback_data="available_courses")],
        [InlineKeyboardButton(text="Мои курсы", callback_data="my_courses")],
        [InlineKeyboardButton(text="Связаться с администратором", callback_data="contact_admin")],
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text="Админ-панель", callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Клавиатура для курсов
def courses_keyboard(courses: list, back_callback: str) -> InlineKeyboardMarkup:
    """Список курсов с кнопкой Назад."""
    buttons = [[InlineKeyboardButton(text=course["title"], callback_data=f"course_{course['id']}")] for course in
               courses]
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=back_callback)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Клавиатура для конкретного курса
async def course_detail_keyboard(course_id: int, user_id: int, from_my_courses: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура для конкретного курса с кнопкой 'Покинуть курс' если пользователь записан на курс."""
    # Проверяем, записан ли пользователь на курс
    is_enrolled = await check_existing_enrollment(user_id, course_id)

    keyboard = [
        [InlineKeyboardButton(text="Информация о курсе", callback_data=f"info_{course_id}")],
        [InlineKeyboardButton(text="Записаться на курс" if not is_enrolled else "Покинуть курс",
                              callback_data=f"{'enroll' if not is_enrolled else 'leave'}_{course_id}")]
    ]

    # Если пришли из меню "Мои курсы", добавляем кнопку "Назад" в главное меню
    if from_my_courses:
        keyboard.append([InlineKeyboardButton(text="Назад", callback_data="my_courses")])
    else:
        keyboard.append([InlineKeyboardButton(text="Назад", callback_data="available_courses")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Функция безопасного обновления сообщения
async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup) -> None:
    """Безопасное обновление сообщения, чтобы избежать ошибок."""
    try:
        await callback.message.edit_text(text=text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Error updating message: {e}")


# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Приветственное сообщение и регистрация/обновление пользователя."""
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    is_admin = telegram_id == ADMIN_USER_ID

    # Создаем или обновляем пользователя
    user = await create_or_update_user(telegram_id=telegram_id, name=name)

    if user:
        # Успешная регистрация или обновление
        await message.answer(
            text=f"Привет, {user['name']}! Выберите действие:",
            reply_markup=main_menu_keyboard(is_admin)
        )
    else:
        # Ошибка при регистрации
        await message.answer(
            text="Произошла ошибка при регистрации. Попробуйте снова."
        )


# Доступные курсы
@dp.callback_query(lambda c: c.data == "available_courses")
async def show_available_courses(callback: CallbackQuery) -> None:
    courses = await fetch_courses()  # Теперь вызываем без аргументов
    await safe_edit_message(
        callback,
        text="Доступные курсы:",
        reply_markup=courses_keyboard(courses, back_callback="main_menu")
    )


# Мои курсы
@dp.callback_query(lambda c: c.data == "my_courses")
async def show_my_courses(callback: CallbackQuery) -> None:
    telegram_id = callback.from_user.id  # Получаем Telegram ID пользователя
    my_courses = await fetch_user_courses(telegram_id)  # Получаем курсы пользователя

    if my_courses:  # Проверим, что курсы есть
        await safe_edit_message(
            callback,
            text="Ваши курсы:",
            reply_markup=courses_keyboard(my_courses, back_callback="main_menu")
        )
    else:
        await safe_edit_message(
            callback,
            text="У вас нет записанных курсов.",
            reply_markup=main_menu_keyboard()
        )


# Детали курса
@dp.callback_query(lambda c: c.data.startswith("course_"))
async def show_course_details(callback: CallbackQuery) -> None:
    course_id = int(callback.data.split("_")[1])
    course = await get_course_by_id(course_id)  # Получаем конкретный курс

    if course:
        # Проверяем, из какого меню пришел запрос (Мои курсы или Доступные курсы)
        from_my_courses = callback.data.startswith("course_")
        await safe_edit_message(
            callback,
            text=f"Курс: {course['title']}",
            reply_markup=await course_detail_keyboard(course_id, callback.from_user.id, from_my_courses)
        )
    else:
        await callback.answer("Курс не найден.", show_alert=True)


# Информация о курсе
@dp.callback_query(lambda c: c.data.startswith("info_"))
async def show_course_info(callback: CallbackQuery) -> None:
    course_id = int(callback.data.split("_")[1])
    course = await get_course_by_id(course_id)
    if course:
        info_text = f"Информация о курсе {course['title']}:\n{course['description']}"
        await safe_edit_message(
            callback,
            text=info_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Назад", callback_data=f"course_{course_id}")]
                ]
            )
        )
    else:
        await callback.answer("Информация недоступна.", show_alert=True)


@dp.callback_query(lambda c: c.data.startswith("enroll_"))
async def enroll_in_course(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[1])
    user_telegram_id = callback.from_user.id

    try:
        user = await get_user_by_telegram_id(user_telegram_id)
        if not user:
            logger.error(f"Пользователь с Telegram ID {user_telegram_id} не найден.")
            await callback.answer("Пользователь не найден. Зарегистрируйтесь через /start.", show_alert=True)
            return

        is_enrolled = await check_existing_enrollment(user['id'], course_id)
        if is_enrolled:
            logger.info(f"Пользователь с Telegram ID {user_telegram_id} уже записан на курс {course_id}.")
            await callback.answer("Вы уже записаны на этот курс.", show_alert=True)
            return

        # Запись на курс
        enrollment = await create_enrollment(user['id'], course_id)
        if enrollment:
            logger.info(f"Пользователь с Telegram ID {user_telegram_id} успешно записан на курс {course_id}.")
            await callback.answer(f"Вы успешно записались на курс: {course_id}!", show_alert=True)
        else:
            logger.error(f"Ошибка при записи пользователя с Telegram ID {user_telegram_id} на курс {course_id}.")
            await callback.answer("Произошла ошибка при записи. Попробуйте позже.", show_alert=True)

    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду: {e}")
        await callback.answer("Ошибка соединения с сервером. Попробуйте позже.", show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка при обработке записи пользователя с Telegram ID {user_telegram_id} на курс {course_id}: {str(e)}")
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)




@dp.callback_query(lambda c: c.data.startswith("leave_"))
async def leave_course(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[1])
    user_telegram_id = callback.from_user.id

    try:
        user = await get_user_by_telegram_id(user_telegram_id)
        if not user:
            logger.error(f"Пользователь с Telegram ID {user_telegram_id} не найден.")
            await callback.answer("Пользователь не найден. Зарегистрируйтесь через /start.", show_alert=True)
            return

        result = await remove_enrollment(user['id'], course_id)
        if result:
            logger.info(f"Пользователь с Telegram ID {user_telegram_id} покинул курс {course_id}.")
            await callback.answer(f"Вы покинули курс: {course_id}.", show_alert=True)
        else:
            logger.error(f"Ошибка при удалении записи пользователя с Telegram ID {user_telegram_id} с курса {course_id}.")
            await callback.answer("Произошла ошибка при удалении. Попробуйте позже.", show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка при обработке запроса пользователя с Telegram ID {user_telegram_id} на удаление с курса {course_id}: {str(e)}")
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)



# Связь с администратором
@dp.callback_query(lambda c: c.data == "contact_admin")
async def contact_admin(callback: CallbackQuery) -> None:
    user_name = callback.from_user.full_name
    user_id = callback.from_user.id
    message = f"Пользователь <a href='tg://user?id={user_id}'>{user_name}</a> хочет связаться."
    await bot.send_message(ADMIN_USER_ID, message, parse_mode="HTML")
    await callback.message.answer("Ваш запрос отправлен администратору.")


# Админ-панель
@dp.callback_query(lambda c: c.data == "admin_panel")
async def admin_panel(callback: CallbackQuery) -> None:
    if callback.from_user.id != ADMIN_USER_ID:
        await callback.answer("У вас нет доступа к этому разделу.", show_alert=True)
    else:
        await safe_edit_message(
            callback,
            text="Добро пожаловать в админ-панель. Функционал будет добавлен позже.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="main_menu")]]
            )
        )


# Обработчик кнопки Назад
@dp.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery) -> None:
    is_admin = callback.from_user.id == ADMIN_USER_ID
    await safe_edit_message(
        callback,
        text="Выберите действие:",
        reply_markup=main_menu_keyboard(is_admin)
    )


# Главная функция
async def main() -> None:
    """Запуск бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
