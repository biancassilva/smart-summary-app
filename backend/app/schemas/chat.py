from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from app.schemas.common import BaseResponse


class ChatMessage(BaseModel):
    """Chat message model"""

    role: Literal["user", "assistant", "system"] = Field(
        ..., description="Message role"
    )
    content: str = Field(..., min_length=1, description="Message content")


class ChatRequest(BaseModel):
    """Chat request model"""

    message: str = Field(..., min_length=1, max_length=50000, description="User message")
    conversation_history: List[ChatMessage] = Field(
        default=[], description="Previous messages"
    )
    model: Optional[str] = Field(default=None, description="OpenAI model to use")
    temperature: Optional[float] = Field(
        default=None, ge=0.0, le=2.0, description="Response creativity"
    )
    max_tokens: Optional[int] = Field(
        default=None, ge=1, le=4000, description="Maximum response tokens"
    )
    stream: bool = Field(default=True, description="Enable streaming response")


class ChatResponse(BaseResponse):
    """Chat response model"""

    response: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None


class StreamingChatResponse(BaseModel):
    """Streaming chat response chunk"""

    content: str
    is_complete: bool = False
    model: str
    usage: Optional[Dict[str, Any]] = None
