FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Загрузка модели spaCy
RUN python -m spacy download ru_core_news_sm

# Загрузка ресурсов NLTK
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Загрузка модели whisper large-v2
RUN python -c "import whisper; whisper.load_model('large-v2')"

# Копирование всего проекта
COPY . .

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
