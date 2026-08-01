from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.trip.constants import TripStatus


class TripCreate(BaseModel):
    title: str = Field(..., max_length=200)
    destination: str = Field(..., max_length=200)
    destination_country: str = Field(..., max_length=100)

    start_date: date
    end_date: date

    duration_days: int = Field(..., ge=1)

    travelers: int = Field(default=1, ge=1)

    budget: Decimal = Field(..., ge=0)

    currency: str = Field(default="USD", max_length=10)

    trip_type: str = Field(..., max_length=50)

    preferences: str | None = Field(default=None, max_length=1000)

    description: str | None = Field(default=None, max_length=500)


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: UUID

    title: str
    destination: str
    destination_country: str

    start_date: date
    end_date: date

    duration_days: int

    travelers: int

    budget: Decimal

    currency: str

    trip_type: str

    preferences: str | None

    description: str | None

    itinerary_json: str | None

    status: TripStatus

    created_at: datetime
    updated_at: datetime