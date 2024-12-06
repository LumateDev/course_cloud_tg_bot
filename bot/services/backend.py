import aiohttp
import logging

async def fetch_courses(endpoint: str, backend_url: str):
    """Получение списка курсов с бэкенда."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{backend_url}/{endpoint}") as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"Ошибка при получении данных с бэкенда: {response.status}")
                return []
