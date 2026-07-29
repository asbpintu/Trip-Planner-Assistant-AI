from decimal import Decimal

from sqlalchemy import DECIMAL, Integer, NVARCHAR
from sqlalchemy.orm import mapped_column, Mapped

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDMixin
from app.modules.trip.constants import TripStatus

from datetime import date
from sqlalchemy import Date
from sqlalchemy import Text, text


class Trip(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "Trips"

    title = mapped_column(
        "Title",
        NVARCHAR(200),
        nullable=False,
    )

    destination = mapped_column(
        "Destination",
        NVARCHAR(200),
        nullable=False,
    )

    destination_country: Mapped[str] = mapped_column(
        "DestinationCountry",
        NVARCHAR(100),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        "StartDate",
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        "EndDate",
        Date,
        nullable=False,
    )

    duration_days = mapped_column(
        "DurationDays",
        Integer,
        nullable=False,
    )

    trip_type: Mapped[str] = mapped_column(
        "TripType",
        NVARCHAR(50),
        nullable=False,
    )

    travelers = mapped_column(
        "Travelers",
        Integer,
        nullable=False,
        server_default=text("1"),
    )

    budget: Mapped[Decimal] = mapped_column(
        "Budget",
        DECIMAL(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        "Currency",
        NVARCHAR(10),
        nullable=False,
        server_default=text("'USD'")
    )

    preferences = mapped_column(
        "Preferences",
        NVARCHAR(1000),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        "Description",
        NVARCHAR(500),
        nullable=True,
    )

    itinerary_json: Mapped[str | None] = mapped_column(
        "ItineraryJson",
        Text,
        nullable=True,
    )

    status = mapped_column(
        "Status",
        NVARCHAR(20),
        nullable=False,
        default=TripStatus.DRAFT.value,
        server_default=text("'Draft'")
    )

    is_deleted: Mapped[bool] = mapped_column(
        "IsDeleted",
        default=False,
        server_default=text("0"),
        nullable=False,
    )