# Используем официальный образ Python как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем весь код в контейнер
COPY ./bot .
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения для работы с dotenv
ARG BOT_TOKEN
ENV BOT_TOKEN=$BOT_TOKEN

ARG BACKEND_URL
ENV BACKEND_URL=$BACKEND_URL

ARG ADMIN_USER_ID
ENV ADMIN_USER_ID=$ADMIN_USER_ID


# Запускаем бота
CMD ["python", "bot.py"]
