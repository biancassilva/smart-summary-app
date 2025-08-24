from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here for Alembic
from app.models.summary import Summary  # noqa
