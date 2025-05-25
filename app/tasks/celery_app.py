from celery import Celery

celery = Celery(
    "marmara_project",
    broker="redis://redis:6379/0",  # URL брокера
    backend="redis://redis:6379/0",  # Хранилище результатов (необязательно)
)

celery.conf.update(
    task_routes={
        "app.tasks.transcribe.process_audio_task": {"queue": "audio"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery.autodiscover_tasks(["app.tasks"])