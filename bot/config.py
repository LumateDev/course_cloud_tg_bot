import logging
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))
# Логгирование
logging.basicConfig(level=logging.INFO)