from app.tasks.transcribe import celery

if __name__ == "__main__":
    celery.start()
