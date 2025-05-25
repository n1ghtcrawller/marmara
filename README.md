# Речевая аналитика Marmara project

## 1. Структура проекта

```
marmara_project/
├── app/
│ ├── init.py
│ ├── main.py # Точка входа FastAPI
│ ├── config.py # Настройки проекта
│ ├── api/
│ │ ├── init.py
│ │ └── endpoints.py # Эндпоинты загрузки и получения результатов
│ ├── services/
│ │ ├── init.py
│ │ ├── speech_service.py # Whisper и трансформация в текст
│ │ ├── audio_service.py # Pydub/librosa: конвертация и длительность
│ │ └── text_service.py # spaCy, NLTK, pymorphy2 анализ текста
│ ├── tasks/
│ │ ├── init.py
│ │ ├── celery_app.py # Инициализация Celery
│ │ └── transcribe.py # Задача на транскрипцию
│ ├── models/
│ │ ├── init.py
│ │ └── db_models.py # SQLAlchemy модели
│ └── database.py # Подключение PostgreSQL
├── celery_worker.py # Точка входа для Celery worker
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 2. Поддержка и запуск

### Шаг 1. Клонировать репозиторий

```bash
git clone https://github.com/yourname/marmara_project.git
cd marmara_project
```

### Шаг 2. Создать файл `.env`

```env
POSTGRES_DB=marmara_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
```

### Шаг 3. Запустить через Docker Compose

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

#### Запуск Celery вручную (если без Docker)
```
celery -A celery_worker.celery worker --loglevel=info
```
Убедитесь, что Redis уже запущен на localhost:6379

### Шаг 4. Использование API

#### Загрузка файла

```http
POST /upload
Content-Type: multipart/form-data
```

Пример с использованием `curl`:

```bash
curl -X POST "http://localhost:8000/upload" -F "file=@example.wav"
```

#### Получение всех расшифровок

```http
GET /transcriptions
```

#### Получение одной расшифровки по ID

```http
GET /transcriptions/{id}
```

## 3. Описание компонентов

* **Whisper** — распознавание речи
* **Pydub/Librosa** — обработка аудио (конвертация, длительность)
* **spaCy, nltk, pymorphy2** — анализ текста (лемматизация, морфология)
* **FastAPI** — REST API
* **Celery** — фоновая обработка задач
* **PostgreSQL** — хранение результатов
* **Redis** — брокер задач для Celery

## 4. Примечания

* Whisper требует GPU для быстрой обработки (поддерживаются и CPU).
* Аудиофайлы временно сохраняются в `/tmp/audio`, могут быть очищены вручную.
* !!! Использовать psycopg2-binary==2.9.10
## 5. Планы

* Добавление веб-интерфейса (React/Vue)
* Расширенная статистика текста (частотный анализ, графы)
* История сессий и скачивание отчётов