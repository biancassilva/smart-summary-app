from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import uuid

from app.models.summary import SummaryStatus
from app.core.config import settings


class SummaryCreateRequest(BaseModel):
    text: str = Field(
        ..., min_length=settings.MIN_TEXT_LENGTH, max_length=settings.MAX_TEXT_LENGTH
    )

    @validator("text")
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v.strip()


class SummaryResponse(BaseModel):
    id: uuid.UUID
    status: SummaryStatus
    summary_text: Optional[str] = None
    error_message: Optional[str] = None
    text_length: int
    summary_length: Optional[int] = None
    processing_time: Optional[float] = None
    model_used: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SummaryListResponse(BaseModel):
    summaries: list[SummaryResponse]
    total: int
    page: int
    per_page: int
