from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, false


from app.modules.trip.models import Trip


class TripRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, trip: Trip) -> Trip:
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)

        return trip

    def get_all(self):

        statement = (
            select(Trip)
            .where(Trip.is_deleted == false())
            .order_by(Trip.created_at.desc())
        )

        return list(self.db.scalars(statement).all())


    def get_by_public_id(
        self,
        public_id: UUID,
    ):

        statement = (
            select(Trip)
            .where(
                Trip.public_id == public_id,
                Trip.is_deleted == false(),
            )
        )

        return self.db.scalar(statement)

    def update(self, trip: Trip) -> Trip:
        self.db.commit()
        self.db.refresh(trip)
        return trip