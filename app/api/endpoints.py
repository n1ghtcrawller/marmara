from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.db_models import Transcription
from app.models.schemas import UserRead
from app.dependencies.auth import get_current_user
from app.tasks.transcribe import process_audio_task

import shutil
import uuid
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    process_audio_task.delay(transcription.id)

    return {"message": "Файл принят", "transcription_id": transcription.id}

@router.get("/results/")
def get_user_transcriptions(
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transcriptions = db.query(Transcription).filter(Transcription.user_id == current_user.id).all()
    return [{"id": t.id, "text": t.text, "created_at": t.created_at} for t in transcriptions]
