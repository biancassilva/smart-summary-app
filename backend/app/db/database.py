from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Create session factory
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
