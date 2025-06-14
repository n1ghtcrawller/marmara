from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
class ReportBase(BaseModel):
    greeting: Optional[bool] = False
    offered_discount: Optional[bool] = False
    offered_special_tariff: Optional[bool] = False
    client_questions: Optional[List[str]] = Field(default_factory=list)
    friendliness_score: Optional[int] = None
    product_interest: Optional[str] = None
    client_objections: Optional[List[str]] = Field(default_factory=list)
    client_knows_source: Optional[bool] = False
    llm_analysis: Optional[str] = None

class ReportCreate(ReportBase):
    transcription_id: int


class ReportOut(ReportBase):
    id: int
    created_at: datetime
    transcription_id: int

    class Config:
        from_attributes = True

class LLMAnalysisUpdate(BaseModel):
    llm_analysis: str