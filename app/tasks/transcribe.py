import os
from app.tasks.celery_app import celery_app
from app.services.audio_service import AudioService
from app.services.speech_service import SpeechService
from app.logger import celery_logger

audio_service = AudioService()
speech_service = SpeechService()

@celery_app.task(
    name="app.tasks.transcribe.process_audio_task",
    bind=True,
    acks_late=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    queue="audio"
)
def process_audio_task(self, input_path: str, use_vad: bool = True) -> dict:
    try:
        celery_logger.info(f"[TASK] Начало обработки файла: {input_path}")

        if use_vad:
            celery_logger.info("VAD включён — применяем VAD к файлу.")
            processed_path = audio_service.process_large_file_with_vad(input_path)
            chunk_paths = [processed_path]
        else:
            celery_logger.info("VAD отключён — разбиваем файл без VAD.")
            chunk_paths = audio_service.split_audio(input_path)
            chunk_paths = [
                audio_service.convert_to_wav(path, os.path.splitext(path)[0] + ".wav")
                for path in chunk_paths
            ]

        result = speech_service.transcribe_chunks(chunk_paths)

        celery_logger.info(f"[TASK] Завершена обработка файла: {input_path}")
        return result

    except Exception as e:
        celery_logger.error(f"[TASK] Ошибка при обработке {input_path}: {e}")
        raise