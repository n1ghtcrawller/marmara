from pydub import AudioSegment
import librosa
import os
import uuid
from app.logger import celery_logger

class AudioService:
    def convert_to_wav(self, input_path: str, output_path: str):
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format="wav")
            celery_logger.info(f"Файл {input_path} конвертирован в {output_path}")
            return output_path
        except Exception as e:
            celery_logger.error(f"Ошибка при конвертации {input_path} в WAV: {e}")
            raise

    def get_duration(self, path: str):
        celery_logger.info(f"Получение длительности файла: {path}")
        y, sr = librosa.load(path)
        duration = librosa.get_duration(y=y, sr=sr)
        celery_logger.info(f"Длительность: {duration} секунд")
        return duration

    def preprocess(self, input_path: str) -> str:
        celery_logger.info(f"Начата предобработка файла: {input_path}")
        ext = os.path.splitext(input_path)[-1]
        if ext.lower() == ".wav":
            celery_logger.info("Файл уже в формате WAV")
            return input_path

        output_path = f"{os.path.splitext(input_path)[0]}_{uuid.uuid4().hex}.wav"
        return self.convert_to_wav(input_path, output_path)
