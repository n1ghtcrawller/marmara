from sqlalchemy.orm import Session
from app.models.db_models import Report
from app.models.schemas import ReportCreate
from typing import List, Optional


def create_report(db: Session, report_data: ReportCreate) -> Report:
    db_report = Report(**report_data.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report_by_transcription(db: Session, transcription_id: int) -> Optional[Report]:
    return db.query(Report).filter(Report.transcription_id == transcription_id).first()


def get_reports(db: Session, skip: int = 0, limit: int = 100) -> List[Report]:
    return db.query(Report).offset(skip).limit(limit).all()


def update_llm_analysis(db: Session, report_id: int, llm_text: str) -> Optional[Report]:
    report = db.query(Report).filter(Report.id == report_id).first()
    if report:
        report.llm_analysis = llm_text
        db.commit()
        db.refresh(report)
    return report


def mark_llm_analysis_as_generating(db: Session, report_id: int) -> Optional[Report]:
    report = db.query(Report).filter(Report.id == report_id).first()
    if report:
        report.llm_analysis = "generating"
        db.commit()
        db.refresh(report)
    return report