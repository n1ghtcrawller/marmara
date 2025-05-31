from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import report as report_crud
from app.models import db_models
from app.services import report_service
from app.models.schemas import ReportCreate, ReportBase, ReportOut
from app.database import SessionLocal
from app.dependencies.auth import get_current_user
from app.models.db_models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/{transcription_id}", response_model=ReportBase)
def generate_report(
    transcription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 Требуется авторизация
):
    transcription = db.query(db_models.Transcription).filter(
        db_models.Transcription.id == transcription_id,
        db_models.Transcription.user_id == current_user.id  # 👈 Проверка владельца
    ).first()

    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")

    report_data = report_service.generate_report_data(transcription.text)
    report_create = ReportCreate(transcription_id=transcription.id, **report_data)

    return report_crud.create_report(db, report_create)


@router.get("/{transcription_id}", response_model=ReportOut)
def get_report(
    transcription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 Требуется авторизация
):
    db_report = report_crud.get_report_by_transcription(db, transcription_id)

    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")

    transcription = db.query(db_models.Transcription).filter(
        db_models.Transcription.id == transcription_id,
        db_models.Transcription.user_id == current_user.id
    ).first()

    if not transcription:
        raise HTTPException(status_code=403, detail="Access denied")

    return db_report


@router.get("/", response_model=list[ReportOut])
def list_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_transcription_ids = db.query(db_models.Transcription.id).filter(
        db_models.Transcription.user_id == current_user.id
    ).subquery()

    return db.query(db_models.Report).filter(
        db_models.Report.transcription_id.in_(user_transcription_ids)
    ).offset(skip).limit(limit).all()
