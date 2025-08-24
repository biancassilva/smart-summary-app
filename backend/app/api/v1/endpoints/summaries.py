from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from app.api.deps import get_db
from app.schemas.summary import (
    SummaryCreateRequest,
    SummaryResponse,
    SummaryListResponse,
)
from app.services.summary_service import SummaryService
from app.models.summary import SummaryStatus
from app.core.exceptions import SummaryNotFoundError, SummaryProcessingError

router = APIRouter()


@router.post("/", response_model=SummaryResponse, status_code=201)
async def create_summary(
    request: SummaryCreateRequest, db: AsyncSession = Depends(get_db)
):
    """Create a new text summary"""
    try:
        service = SummaryService(db)
        return await service.create_summary(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{summary_id}", response_model=SummaryResponse)
async def get_summary(summary_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a summary by ID"""
    try:
        service = SummaryService(db)
        return await service.get_summary(summary_id)
    except SummaryNotFoundError:
        raise HTTPException(status_code=404, detail="Summary not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=SummaryListResponse)
async def list_summaries(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[SummaryStatus] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db),
):
    """List summaries with pagination and optional status filtering"""
    try:
        service = SummaryService(db)
        return await service.list_summaries(page=page, per_page=per_page, status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
