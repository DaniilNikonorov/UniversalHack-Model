# Берем нужный базовый образ
FROM python:3.10.5
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app

RUN apk add --no-cache \
    g++ \
    gcc \
    make \
    gfortran \
    musl-dev \
    python3-dev

# Устанавливаем все зависимости
RUN python -m pip install --upgrade pip
RUN pip install ruff pytest
RUN pip install -U "ray[default]==2.6.3"

RUN pip install pandas
# RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r ./requirements.txt
# Говорим контейнеру какой порт слушай
EXPOSE 8080
# Запуск нашего приложения при старте контейнера
CMD python /app/prediction.py