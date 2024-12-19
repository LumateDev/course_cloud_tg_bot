import logging
import aiohttp

from config import BACKEND_URL

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Универсальная функция для отправки GET-запросов
async def fetch_data(endpoint: str):
    """Получение данных с бэкенда."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/{endpoint}") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Успешно получены данные с бэкенда: {len(data)} записей.")
                    return data
                else:
                    logger.error(f"Ошибка при получении данных с бэкенда: {response.status}")
                    return []
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду: {e}")
        return []


# Получение списка курсов
async def fetch_courses():
    """Получение списка курсов с бэкенда."""
    return await fetch_data("courses/")

# Получение курса по ID
async def get_course_by_id(course_id: int):
    """Получение информации о курсе по ID."""
    return await fetch_data(f"courses/{course_id}")

# Получение пользователя по Telegram ID
async def get_user_by_telegram_id(telegram_id: int):
    """Получение пользователя по его Telegram ID."""
    return await fetch_data(f"users/{telegram_id}")

# Создание или обновление пользователя
async def create_or_update_user(telegram_id: int, name: str):
    """Создать или обновить пользователя на бэкенде по Telegram ID."""
    data = {"telegram_id": telegram_id, "name": name}
    return await post_data("users", data)

# Получение курсов для пользователя по Telegram ID через записи
# Получение курсов для пользователя по Telegram ID
async def fetch_user_courses(telegram_id: int):
    """Получение курсов для пользователя по Telegram ID через записи на курсы."""
    try:
        # Получаем информацию о пользователе
        user = await get_user_by_telegram_id(telegram_id)
        if not user:
            logger.error(f"Пользователь с Telegram ID {telegram_id} не найден.")
            return []

        # Получаем курсы пользователя
        courses = await fetch_data(f"enrollments/users/{telegram_id}/courses")
        logger.info(f"Получено {len(courses)} курсов для пользователя с Telegram ID {telegram_id}.")
        return courses

    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду для получения курсов пользователя с Telegram ID {telegram_id}: {e}")
        return []


# Создание записи о записи пользователя на курс
# Создание записи о записи пользователя на курс
async def create_enrollment(user_id: int, course_id: int):
    data = {"user_id": user_id, "course_id": course_id}
    response = await post_data("enrollments/enroll", data)

    if response.get("detail") == "User already enrolled in this course":
        logger.info(f"Пользователь с ID {user_id} уже записан на курс {course_id}.")
        return None  # Пользователь уже записан, возвращаем None

    if response.get(
            "status") == "success":
        logger.info(f"Успешно записан пользователь с ID {user_id} на курс {course_id}.")
        return response  # Возвращаем успешный ответ
    return None  # Ошибка записи


# Универсальная функция для отправки POST-запросов
async def post_data(endpoint: str, data: dict):
    """Отправка данных на бэкенд."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/{endpoint}", json=data) as response:
                logger.info(f"Ответ от сервера: {response.status} для запроса {endpoint} с данными {data}")
                print(f"response.status: {response.status}")
                if response.status == 200 or response.status == 201:
                    response_data = await response.json()
                    logger.info(f"Успешно отправлены данные на бэкенд: {response.status}, {response_data}")
                    return response_data
                else:
                    logger.error(f"Ошибка при отправке данных на бэкенд: {response.status}, {await response.text()}")
                    return {}
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду: {e}")
        return {}


# Универсальная функция для отправки DELETE-запросов
async def delete_data(endpoint: str):
    """Отправка DELETE-запроса на бэкенд."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{BACKEND_URL}/{endpoint}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка при удалении данных на бэкенде: {response.status}")
                    return {}
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду для удаления данных: {e}")
        return {}


async def remove_enrollment(user_id: int, course_id: int):
    try:
        response = await delete_data(f"enrollments/leave_enrollment/{user_id}/{course_id}")
        return response.get("status") == "success"
    except Exception as e:
        logger.error(f"Ошибка при удалении записи: {str(e)}")
        return False



# Проверка существующей записи на курс
async def check_existing_enrollment(user_id: int, course_id: int) -> bool:
    """Проверить, записан ли пользователь на курс."""
    courses = await fetch_user_courses(user_id)
    for course in courses:
        if course['id'] == course_id:
            logger.info(f"Пользователь с ID {user_id} уже записан на курс с ID {course_id}.")
            return True
    return False
