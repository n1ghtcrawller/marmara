from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON
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


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    transcription_id = Column(Integer, ForeignKey("transcriptions.id"), nullable=True)

    greeting = Column(Boolean, default=False)
    offered_discount = Column(Boolean, default=False)
    offered_special_tariff = Column(Boolean, default=False)
    client_questions = Column(JSON)  # список вопросов клиента
    friendliness_score = Column(Integer)
    product_interest = Column(String(255))
    client_objections = Column(JSON)
    client_knows_source = Column(Boolean, default=False)
    llm_analysis = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    transcription = relationship("Transcription", backref="report")