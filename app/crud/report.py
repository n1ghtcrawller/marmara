from sqlalchemy.orm import Session
from app.models.db_models import Report
from app.models.schemas import ReportCreate

def create_report(db: Session, report_data: ReportCreate):
    db_report = Report(**report_data.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report_by_transcription(db: Session, transcription_id: int):
    return db.query(Report).filter(Report.transcription_id == transcription_id).first()


def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()
