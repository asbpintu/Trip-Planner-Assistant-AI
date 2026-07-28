from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(
    db: Session = Depends(get_db),
):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "application": "Trip Planner Assistant AI",
            "version": "1.0.0",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "healthy",
            "application": "Trip Planner Assistant AI",
            "version": "1.0.0",
            "database": "disconnected",
            "error": str(e),
        }