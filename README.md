# Речевая аналитика Marmara project

## 1. Структура проекта

```
marmara_project/
├── app/                      # Основной backend код FastAPI
│   ├── main.py               # Точка входа FastAPI
│   ├── config.py             # Конфигурация проекта
│   ├── logger.py             # Логгер
│   ├── database.py           # Подключение PostgreSQL
│   ├── api/                  # API эндпоинты
│   │   ├── endpoints.py      # Эндпоинты: загрузка файлов, получение метрик
│   │   └── auth.py           # Авторизация
│   ├── core/                 # Безопасность, авторизация
│   │   └── security.py       # JWT, пароли
│   ├── dependencies/         # Зависимости FastAPI
│   │   └── auth.py
│   ├── models/               # Схемы и модели БД
│   │   ├── db_models.py      # SQLAlchemy модели
│   │   └── schemas.py        # Pydantic-схемы
│   ├── services/             # Логика обработки данных
│   │   ├── audio_service.py              # Обработка и анализ аудио (pydub, librosa)
│   │   ├── speech_service.py             # Работа с Whisper
│   │   ├── whisper_model.py              # Загрузка и кэширование Whisper модели
│   │   ├── text_service.py               # Морфология и очистка текста (spaCy, nltk, pymorphy2)
│   │   ├── transcription_parser.py       # Парсинг транскрипции
│   │   ├── metrics_service.py            # Вычисление текстовых метрик
│   │   └── text_metrics.service.py       # Расширенный анализ текста
│   └── tasks/                # Celery задачи
│       ├── celery_app.py     # Инициализация Celery
│       ├── transcribe.py     # Асинхронная транскрипция и анализ
│       └── audio.task.py     # Асинхронная обработка аудиофайлов
│
├── celery_worker.py          # Запуск Celery воркера
├── requirements.txt          # Зависимости проекта
├── Dockerfile                # Docker образ backend
├── docker-compose.yml        # docker-compose для разворачивания
├── docker_cache/             # Предзагруженная Whisper модель
│   └── whisper/large-v2.pt   # Модель whisper large-v2
├── marmara_frontend/         # Next.js + Tailwind frontend
├── uploaded_files/           # Папка для загружаемых пользователями файлов
└── README.md                 # Этот файл

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
### 🚀 Быстрый старт
#### 🔧 Установка с Docker
####  Собрать и запустить контейнер
```bash
docker-compose up --build
```
#### 📦 Убедись, что файл модели large-v2.pt находится в docker_cache/whisper/large-v2.pt

#### Если файл не загружен — скачай вручную:
```bash
mkdir -p docker_cache/whisper
python -c "import whisper; whisper.load_model('large-v2')"
cp ~/.cache/whisper/large-v2.pt docker_cache/whisper/ #если на windows, то  путь из папки корневого пользователя
```
Приложение будет доступно по адресу: [http://localhost](http://localhost)

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

* Расширенная статистика текста (частотный анализ, графы)
* Сделать сводку по всем записям
* Сделать мониторинг и по сотрудникам
* Сделать мини аккаунты - для сотрудников, которым будут доступны ,только их записи
* Сделать аккаунты для партнеров