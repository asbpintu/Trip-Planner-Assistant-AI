from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class UUIDMixin:
    id: Mapped[str] = mapped_column(
        "Id",
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid4,
    )

    public_id: Mapped[str] = mapped_column(
        "PublicId",
        UNIQUEIDENTIFIER,
        default=uuid4,
        unique=True,
        nullable=False,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        "CreatedAt",
        DateTime,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        "UpdatedAt",
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )