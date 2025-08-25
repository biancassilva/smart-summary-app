from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model"""

    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.utcnow()


class ErrorResponse(BaseModel):
    """Error response model"""

    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()


class HealthResponse(BaseResponse):
    """Health check response"""

    status: str
    version: str
    environment: str
