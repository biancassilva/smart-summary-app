from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        message="Service is running properly",
    )


@router.get("/health/ready")
async def readiness_check():
    """Readiness check for deployment"""
    return {"status": "ready"}


@router.get("/health/live")
async def liveness_check():
    """Liveness check for deployment"""
    return {"status": "alive"}
