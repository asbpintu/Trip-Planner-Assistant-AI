from app.modules import trip
from app.modules.trip.constants import TripStatus
from app.modules.trip.models import Trip
from app.modules.trip.repository import TripRepository
from app.modules.trip.schemas import TripCreate
from uuid import UUID

import json
from fastapi import HTTPException
from app.modules.ai.groq_service import GroqService
from app.modules.ai.prompt_builder import PromptBuilder



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

    def generate_itinerary(
        self,
        public_id,
    ):

        trip = self.repository.get_by_public_id(public_id)

        if trip is None:
            raise HTTPException(
                status_code=404,
                detail="Trip not found",
            )

        prompt = PromptBuilder.build_trip_prompt(trip)

        groq = GroqService()

        response = groq.generate(prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="AI returned invalid JSON.",
            )

        trip.itinerary_json = json.dumps(
            parsed,
            indent=2,
            ensure_ascii=False,
        )

        trip.status = "Generated"

        self.repository.update(trip)

        return trip