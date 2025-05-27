from app.database import SessionLocal
from app.models.db_models import Transcription
from app.services.speech_service import SpeechService
from app.services.audio_service import AudioService
from app.logger import celery_logger
from app.tasks.celery_app import celery

@celery.task(bind=True, acks_late=True, autoretry_for=(Exception,), retry_backoff=True)
def process_audio_task(self, transcription_id: int):
    db = SessionLocal()
    try:
        celery_logger.info(f"Начата обработка транскрипции с ID {transcription_id}")
        transcription = db.query(Transcription).get(transcription_id)
        if not transcription:
            celery_logger.warning(f"Транскрипция с ID {transcription_id} не найдена")
            return

        audio_path = transcription.file_path
        celery_logger.info(f"Обработка файла: {audio_path}")

        processed_path = AudioService().preprocess(audio_path)
        celery_logger.info(f"Файл после предобработки: {processed_path}")

        result = SpeechService().transcribe(processed_path)
        raw_text = result["text"]
        metrics = result["metrics"]

        celery_logger.info(f"Сырой текст: {raw_text}")

        transcription.text = raw_text
        transcription.language = metrics.get("language")
        transcription.duration_sec = metrics.get("duration_sec")
        transcription.word_count = metrics.get("word_count")
        transcription.segment_count = metrics.get("segment_count")
        transcription.avg_segment_duration_sec = metrics.get("avg_segment_duration_sec")
        transcription.avg_logprob = metrics.get("avg_logprob")
        transcription.silence_ratio = metrics.get("silence_ratio")

        db.commit()
        celery_logger.info(f"Транскрипция ID {transcription_id} успешно сохранена")
    except Exception as e:
        celery_logger.error(f"Ошибка при обработке транскрипции ID {transcription_id}: {e}")
    finally:
        db.close()
