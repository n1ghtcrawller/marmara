from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Request
from app.services.file_service import FileService
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.db_models import Transcription
from app.models.schemas import UserRead
from app.dependencies.auth import get_current_user
from app.tasks.transcribe import process_audio_task
from app.logger import celery_logger
from app.services.metrics_service import collect_metrics
from pathlib import Path
import shutil
import uuid
import os
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
file_service = FileService(upload_dir=UPLOAD_DIR)

@router.post("/upload/")
async def upload_audio(
    file: UploadFile = File(...),
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Сохраняем запись в базу
    transcription = Transcription(file_path=file_path, user_id=current_user.id)
    db.add(transcription)
    db.commit()
    db.refresh(transcription)

    # Запускаем фоновую задачу
    celery_logger.info(f"Отправка задачи Celery для ID {transcription.id}")
    process_audio_task.delay(transcription.id)
    return {"message": "Файл принят", "transcription_id": transcription.id}

@router.get("/results/")
def get_user_transcriptions(
    request: Request,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transcriptions = db.query(Transcription).filter(Transcription.user_id == current_user.id).all()

    results = []
    for t in transcriptions:
        try:
            text_data = json.loads(t.text) if t.text else None
        except json.JSONDecodeError:
            text_data = t.text

        audio_url = request.url_for("serve_audio_file", filename=os.path.basename(t.file_path))

        results.append({
            "id": t.id,
            "text": text_data,
            "created_at": t.created_at,
            "audio_url": audio_url
        })

    return results

@router.delete("/results/{transcription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transcription(
    transcription_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transcription = db.query(Transcription).filter(
        Transcription.id == transcription_id,
        Transcription.user_id == current_user.id
    ).first()

    if not transcription:
        raise HTTPException(status_code=404, detail="Расшифровка не найдена")
    if transcription.file_path and os.path.exists(transcription.file_path):
        try:
            os.remove(transcription.file_path)
        except Exception as e:
            celery_logger.warning(f"Не удалось удалить файл {transcription.file_path}: {e}")

    db.delete(transcription)
    db.commit()


@router.get("/metrics/")
def get_transcription_metrics(
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return collect_metrics(current_user.id, db)

@router.get("/audio/{filename}", name="serve_audio_file")
def serve_audio_file(filename: str):
    return file_service.get_file_response(filename)