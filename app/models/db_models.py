from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transcriptions = relationship("Transcription", back_populates="owner")


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    language = Column(String, nullable=True)
    duration_sec = Column(Float, nullable=True)
    word_count = Column(Integer, nullable=True)
    segment_count = Column(Integer, nullable=True)
    avg_segment_duration_sec = Column(Float, nullable=True)
    avg_logprob = Column(Float, nullable=True)
    silence_ratio = Column(Float, nullable=True)

    owner = relationship("User", back_populates="transcriptions")

class AudioResult(Base):
    __tablename__ = "audio_results"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    language = Column(String)
    audio_duration = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_type = Column(String)