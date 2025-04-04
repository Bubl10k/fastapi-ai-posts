from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
