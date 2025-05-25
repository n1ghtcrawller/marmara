from app.database import SessionLocal
from app.models.db_models import Transcription
from app.services.speech_service import SpeechService
from app.services.audio_service import AudioService
from app.services.text_service import TextService

from app.tasks.celery_app import celery

@celery.task
def process_audio_task(transcription_id: int):
    db = SessionLocal()
    try:
        transcription = db.query(Transcription).get(transcription_id)
        if not transcription:
            return

        # Обработка
        audio_path = transcription.file_path
        processed_path = AudioService.preprocess(audio_path)
        raw_text = SpeechService().transcribe(processed_path)
        analyzed_text = TextService().analyze(raw_text)

        transcription.text = analyzed_text
        db.commit()
    finally:
        db.close()
