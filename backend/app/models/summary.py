from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.db.base import Base


class SummaryStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_text = Column(Text, nullable=False)
    summary_text = Column(Text, nullable=True)
    status = Column(Enum(SummaryStatus), default=SummaryStatus.PENDING, nullable=False)
    error_message = Column(String(500), nullable=True)

    # Metadata
    text_length = Column(Integer, nullable=False)
    summary_length = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)  # seconds
    model_used = Column(String(50), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Summary {self.id}: {self.status}>"
