from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.trip.repository import TripRepository
from app.modules.trip.schemas import TripCreate, TripResponse
from app.modules.trip.service import TripService

from uuid import UUID
from fastapi import HTTPException

router = APIRouter()


@router.post(
    "",
    response_model=TripResponse,
    status_code=201,
)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db),
):

    repository = TripRepository(db)

    service = TripService(repository)

    created_trip = service.create_trip(trip)

    return created_trip


@router.get(
    "",
    response_model=list[TripResponse],
)
def get_all_trips(
    db: Session = Depends(get_db),
):

    repository = TripRepository(db)

    service = TripService(repository)

    return service.get_all_trips()


@router.get(
    "/{public_id}",
    response_model=TripResponse,
)
def get_trip(
    public_id: UUID,
    db: Session = Depends(get_db),
):

    repository = TripRepository(db)

    service = TripService(repository)

    trip = service.get_trip(public_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    return trip


@router.post(
    "/{public_id}/generate",
    response_model=TripResponse,
)
def generate_trip(
    public_id: UUID,
    db: Session = Depends(get_db),
):

    repository = TripRepository(db)

    service = TripService(repository)

    return service.generate_itinerary(public_id)