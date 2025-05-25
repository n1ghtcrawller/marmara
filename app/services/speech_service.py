import whisper
from app.logger import celery_logger

class SpeechService:
    def __init__(self, model_name="base"):
        celery_logger.info(f"Загрузка модели Whisper: {model_name}")
        self.model = whisper.load_model(model_name)
        celery_logger.info("Модель загружена")

    def transcribe(self, filepath):
        celery_logger.info(f"Начата транскрипция файла: {filepath}")
        result = self.model.transcribe(filepath)
        celery_logger.info("Транскрипция завершена")
        return result['text']
