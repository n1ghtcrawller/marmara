from celery import Celery

celery = Celery(
    "marmara_project",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery.conf.update(
    task_routes={
        "app.tasks.audio_task.process_audio_task": {"queue": "audio"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery.autodiscover_tasks(["app.tasks"])
