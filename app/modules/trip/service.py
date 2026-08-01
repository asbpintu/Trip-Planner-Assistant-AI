from app.modules.trip.constants import TripStatus
from app.modules.trip.models import Trip
from app.modules.trip.repository import TripRepository
from app.modules.trip.schemas import TripCreate
from uuid import UUID



class TripService:

    def __init__(self, repository: TripRepository):
        self.repository = repository

    def create_trip(self, data: TripCreate) -> Trip:

        trip = Trip(
            **data.model_dump(),
            status=TripStatus.DRAFT.value,
        )

        return self.repository.create(trip)

    def get_all_trips(self):
        return self.repository.get_all()


    def get_trip(self, public_id: UUID):
        return self.repository.get_by_public_id(public_id)