FROM python:3.10-slim

# Установим ffmpeg и git
RUN apt-get update && apt-get install -y ffmpeg git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только requirements.txt сначала — это кэшируется отдельно
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (включая /app, uploaded_files и т.п.)
COPY . .

# Добавляем заранее загруженную модель Whisper
COPY docker_cache/whisper/large-v2.pt /root/.cache/whisper/large-v2.pt

# Команда по умолчанию
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
