import torchaudio
from app.logger import celery_logger
from app.services.whisper_model import get_whisper_model
from typing import List
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

    def transcribe_chunks(self, chunk_paths: List[str]) -> dict:
        full_text = ""
        all_segments = []
        all_words = 0
        total_duration = 0.0
        total_logprob = 0.0
        total_silence_segments = 0
        total_segment_count = 0
        language = None

        for path in chunk_paths:
            try:
                celery_logger.info(f"Транскрипция чанка: {path}")
                result = self.model.transcribe(path)

                chunk_segments = result.get("segments", [])
                all_segments.extend(chunk_segments)
                full_text += result.get("text", "") + " "

                chunk_word_count = len(result.get("text", "").split())
                all_words += chunk_word_count
                total_segment_count += len(chunk_segments)

                total_logprob += sum(s.get("avg_logprob", 0) for s in chunk_segments)
                total_silence_segments += len([s for s in chunk_segments if s.get("no_speech_prob", 0) > 0.5])

                audio_info = torchaudio.info(path)
                total_duration += audio_info.num_frames / audio_info.sample_rate

                if not language:
                    language = result.get("language")

            except Exception as e:
                celery_logger.warning(f"Ошибка транскрипции чанка {path}: {e}")

        avg_segment_duration = (
            sum(s['end'] - s['start'] for s in all_segments) / total_segment_count
            if total_segment_count > 0 else 0
        )

        avg_logprob = (
            total_logprob / total_segment_count if total_segment_count > 0 else 0
        )

        silence_ratio = (
            total_silence_segments / total_segment_count if total_segment_count > 0 else 0
        )

        metrics = {
            "language": language,
            "duration_sec": round(total_duration, 2),
            "word_count": all_words,
            "segment_count": total_segment_count,
            "avg_segment_duration_sec": round(avg_segment_duration, 2),
            "avg_logprob": round(avg_logprob, 3),
            "silence_ratio": round(silence_ratio, 3),
        }

        return {
            "text": full_text.strip(),
            "metrics": metrics,
        }

    def _merge_transcriptions(self, results: list):
        full_text = " ".join(r['text'] for r in results)
        segment_count = sum(r['metrics']['segment_count'] for r in results)
        total_duration = sum(r['metrics']['duration_sec'] for r in results if r['metrics']['duration_sec'])
        total_words = sum(r['metrics']['word_count'] for r in results)

        avg_segment_duration = (
            sum(r['metrics']['avg_segment_duration_sec'] * r['metrics']['segment_count']
                for r in results) / segment_count
            if segment_count else 0
        )
        avg_logprob = (
            sum(r['metrics']['avg_logprob'] * r['metrics']['segment_count']
                for r in results) / segment_count
            if segment_count else 0
        )
        silence_ratio = (
            sum(r['metrics']['silence_ratio'] * r['metrics']['segment_count']
                for r in results) / segment_count
            if segment_count else 0
        )

        language = results[0]['metrics'].get('language') if results else "unknown"

        return {
            "text": full_text.strip(),
            "metrics": {
                "language": language,
                "duration_sec": round(total_duration, 2),
                "word_count": total_words,
                "segment_count": segment_count,
                "avg_segment_duration_sec": round(avg_segment_duration, 2),
                "avg_logprob": round(avg_logprob, 3),
                "silence_ratio": round(silence_ratio, 3),
            }
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




