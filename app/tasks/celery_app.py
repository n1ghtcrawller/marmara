from celery import Celery

celery_app = Celery(
    "marmara_project",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks.transcribe", "app.tasks.analyze_llm"]

)

celery_app.conf.update(
    task_routes={
        "app.tasks.transcribe.process_audio_task": {"queue": "audio"},
        "app.tasks.analyze_llm.analyze_llm_task": {"queue": "llm"},
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,

)

celery_app.autodiscover_tasks(["app.tasks"])
