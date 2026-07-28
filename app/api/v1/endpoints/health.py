from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "Trip Planner Assistant AI",
        "version": "1.0.0",
    }