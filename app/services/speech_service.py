import torchaudio
from app.logger import celery_logger
from app.services.whisper_model import get_whisper_model

class SpeechService:
    def __init__(self):
        self.model = get_whisper_model()
        celery_logger.info("Модель Whisper загружена и готова к использованию")

    def transcribe(self, filepath):
        celery_logger.info(f"Начата транскрипция файла: {filepath}")
        try:
            result = self.model.transcribe(filepath)
            celery_logger.info("Транскрипция завершена")
        except Exception as e:
            celery_logger.error(f"Ошибка транскрипции Whisper: {e}")
            raise

        metrics = self._extract_metrics(result, filepath)
        for key, value in metrics.items():
            celery_logger.info(f"{key}: {value}")

        return {
            "text": result['text'],
            "metrics": metrics
        }

    def _extract_metrics(self, result, filepath):
        try:
            audio_info = torchaudio.info(filepath)
            duration = audio_info.num_frames / audio_info.sample_rate
        except Exception as e:
            celery_logger.warning(f"Не удалось определить длительность аудио: {e}")
            duration = None

        text = result.get('text', "")
        segments = result.get('segments', [])
        segment_count = len(segments)
        total_words = len(text.split())

        avg_segment_duration = (
            sum(s['end'] - s['start'] for s in segments) / segment_count
            if segment_count > 0 else 0
        )

        avg_logprob = (
            sum(s.get('avg_logprob', 0) for s in segments) / segment_count
            if segment_count > 0 else 0
        )

        silence_ratio = (
            len([s for s in segments if s.get('no_speech_prob', 0) > 0.5]) / segment_count
            if segment_count > 0 else 0
        )

        return {
            "language": result.get("language"),
            "duration_sec": round(duration, 2) if duration else None,
            "word_count": total_words,
            "segment_count": segment_count,
            "avg_segment_duration_sec": round(avg_segment_duration, 2),
            "avg_logprob": round(avg_logprob, 3),
            "silence_ratio": round(silence_ratio, 3),
        }
