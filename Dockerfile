# Берем нужный базовый образ
FROM python:3.10.5
# Копируем все файлы из текущей директории в /app контейнера
COPY ./ /app
# RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
COPY requirements.txt .

# Устанавливаем все зависимости
RUN python -m pip install --upgrade pip
RUN pip install ruff pytest
RUN pip install -U "ray[default]==2.6.3"
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pandas
WORKDIR /app
# RUN pip install -r ./requirements.txt
# Запуск нашего приложения при старте контейнера
CMD /app/prediction.py