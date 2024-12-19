# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY ./backend .
COPY ./requirements.txt .


# Устанавливаем рабочие зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Экспонируем порт для приложения FastAPI
EXPOSE 8000

# Устанавливаем переменную окружения для использования сертификата
ARG SSL_CERT_PATH
ARG DATABASE_URL

ENV SSL_CERT_PATH = $SSL_CERT_PATH
ENV DATABASE_URL = $DATABASE_URL

# Запускаем сервер с помощью uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
