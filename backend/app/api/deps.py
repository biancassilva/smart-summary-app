from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import SessionLocal


async def get_db() -> AsyncSession:
    """Database dependency"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
