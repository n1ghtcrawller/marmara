from app.database import SessionLocal
from app.crud.report import update_llm_analysis
from app.services.report_service import analyze_openrouter_llm
from app.models.db_models import Report, Transcription
from app.logger import celery_logger
from app.tasks.celery_app import celery_app

@celery_app.task(
    bind=True,
    name="app.tasks.analyze_llm.analyze_llm_task",
    autoretry_for=(Exception,),
    retry_backoff=True,
    queue="llm"
)
def analyze_llm_task(self, report_id: int):
    db = SessionLocal()
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            celery_logger.warning(f"Report {report_id} not found")
            return

        transcription = db.query(Transcription).filter(Transcription.id == report.transcription_id).first()
        if not transcription:
            celery_logger.warning(f"Transcription {report.transcription_id} not found")
            return

        llm_result = analyze_openrouter_llm(transcription.text)
        update_llm_analysis(db, report_id, llm_result)
        celery_logger.info(f"LLM-анализ завершён для отчёта {report_id}")
    except Exception as e:
        celery_logger.error(f"Ошибка при анализе LLM: {e}")
    finally:
        db.close()
