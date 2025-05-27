from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models.db_models import Transcription

def collect_metrics(user_id: int, db: Session, days: int = 7):
    since_date = datetime.utcnow() - timedelta(days=days - 1)

    transcriptions = (
        db.query(Transcription)
        .filter(Transcription.user_id == user_id)
        .filter(Transcription.created_at >= since_date)
        .all()
    )

    uploads_per_day = defaultdict(int)
    length_buckets = defaultdict(int)
    language_counts = defaultdict(int)
    analysis_type_counts = defaultdict(int)

    for t in transcriptions:
        date_key = t.created_at.date().isoformat()
        uploads_per_day[date_key] += 1

        duration = t.duration_sec
        if duration is not None:
            if duration < 60:
                length_buckets["< 1 мин"] += 1
            elif duration <= 300:
                length_buckets["1–5 мин"] += 1
            elif duration <= 900:
                length_buckets["5–15 мин"] += 1
            else:
                length_buckets["> 15 мин"] += 1

        lang = t.language or "неизвестно"
        language_counts[lang] += 1

        analysis_type = "стандартный"
        analysis_type_counts[analysis_type] += 1

    uploads_chart = [
        {
            "date": (since_date + timedelta(days=i)).date().isoformat(),
            "count": uploads_per_day.get((since_date + timedelta(days=i)).date().isoformat(), 0)
        }
        for i in range(days)
    ]

    return {
        "uploads_per_day": uploads_chart,
        "length_distribution": [{"range": k, "count": v} for k, v in length_buckets.items()],
        "languages": [{"name": k, "value": v} for k, v in language_counts.items()],
        "analysis_types": [{"type": k, "count": v} for k, v in analysis_type_counts.items()],
    }
