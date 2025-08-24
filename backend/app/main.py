from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import engine
from app.db.base import Base
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.monitoring import PrometheusMiddleware

# Setup logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    # Startup
    logger.info("Starting up Text Summarization API")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown
    logger.info("Shutting down Text Summarization API")
    await engine.dispose()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="A scalable API for text summarization using OpenAI",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(PrometheusMiddleware)

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()
