import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime
import structlog

from app.models.summary import Summary, SummaryStatus
from app.schemas.summary import (
    SummaryCreateRequest,
    SummaryResponse,
    SummaryListResponse,
)
from app.services.openai_service import OpenAIService
from app.core.exceptions import SummaryNotFoundError, SummaryProcessingError

logger = structlog.get_logger()


class SummaryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.openai_service = OpenAIService()

    async def create_summary(self, request: SummaryCreateRequest) -> SummaryResponse:
        """Create a new summary request"""

        # Create summary record
        summary = Summary(
            original_text=request.text,
            text_length=len(request.text),
            status=SummaryStatus.PENDING,
        )

        self.db.add(summary)
        await self.db.commit()
        await self.db.refresh(summary)

        logger.info("Summary request created", summary_id=summary.id)

        # Process summary asynchronously in background
        await self._process_summary_async(summary.id)

        return SummaryResponse.from_orm(summary)

    async def get_summary(self, summary_id: uuid.UUID) -> SummaryResponse:
        """Get a summary by ID"""

        result = await self.db.execute(select(Summary).where(Summary.id == summary_id))
        summary = result.scalar_one_or_none()

        if not summary:
            raise SummaryNotFoundError(f"Summary with ID {summary_id} not found")

        return SummaryResponse.from_orm(summary)

    async def list_summaries(
        self, page: int = 1, per_page: int = 20, status: Optional[SummaryStatus] = None
    ) -> SummaryListResponse:
        """List summaries with pagination"""

        query = select(Summary).order_by(desc(Summary.created_at))

        if status:
            query = query.where(Summary.status == status)

        # Count total records
        count_query = select(func.count(Summary.id))
        if status:
            count_query = count_query.where(Summary.status == status)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await self.db.execute(query)
        summaries = result.scalars().all()

        return SummaryListResponse(
            summaries=[SummaryResponse.from_orm(s) for s in summaries],
            total=total,
            page=page,
            per_page=per_page,
        )

    async def _process_summary_async(self, summary_id: uuid.UUID):
        """Process summary in the background"""
        try:
            # Update status to processing
            await self._update_summary_status(summary_id, SummaryStatus.PROCESSING)

            # Get summary record
            result = await self.db.execute(
                select(Summary).where(Summary.id == summary_id)
            )
            summary = result.scalar_one()

            # Generate summary using OpenAI
            summary_text, processing_time = await self.openai_service.summarize_text(
                summary.original_text
            )

            # Update summary with results
            summary.summary_text = summary_text
            summary.summary_length = len(summary_text)
            summary.processing_time = processing_time
            summary.model_used = settings.OPENAI_MODEL
            summary.status = SummaryStatus.COMPLETED
            summary.completed_at = datetime.utcnow()

            await self.db.commit()

            logger.info("Summary processed successfully", summary_id=summary_id)

        except Exception as e:
            logger.error(
                "Failed to process summary", summary_id=summary_id, error=str(e)
            )

            # Update summary with error
            await self._update_summary_status(
                summary_id, SummaryStatus.FAILED, error_message=str(e)[:500]
            )

            raise SummaryProcessingError(f"Failed to process summary: {str(e)}")

    async def _update_summary_status(
        self,
        summary_id: uuid.UUID,
        status: SummaryStatus,
        error_message: Optional[str] = None,
    ):
        """Update summary status"""
        result = await self.db.execute(select(Summary).where(Summary.id == summary_id))
        summary = result.scalar_one()

        summary.status = status
        if error_message:
            summary.error_message = error_message

        await self.db.commit()
