# Берем нужный базовый образ
FROM python:3.10-alpine
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
# Устанавливаем все зависимости
RUN python -m pip install --upgrade pip
RUN pip install ruff pytest
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
# Говорим контейнеру какой порт слушай
EXPOSE 8080
# Запуск нашего приложения при старте контейнера
CMD python /app/prediction.py