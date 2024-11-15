import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
import requests
from datetime import datetime
import logging

load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')
BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print(BACKEND_URL)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())