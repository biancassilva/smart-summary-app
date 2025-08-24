from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

from app.api.deps import get_db
from app.core.config import settings

router = APIRouter()
logger = structlog.get_logger()


@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check including database connectivity"""
    health_status = {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "checks": {},
    }

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["checks"]["database"] = "unhealthy"
        health_status["status"] = "degraded"

    # OpenAI API check (optional - might want to skip to avoid API costs)
    health_status["checks"]["openai"] = "not_checked"

    return health_status
