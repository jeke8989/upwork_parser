# Указываем базовый образ
FROM python:3.10-slim

# Ставим виртуальный дисплей
RUN apt-get update -y
RUN apt-get install xvfb -y

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Ставим вебдрайвер
RUN playwright install chromium --with-deps

# Копируем остальные файлы проекта
COPY . .

ENTRYPOINT xvfb-run -a python main.py