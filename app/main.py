from fastapi import FastAPI

from app.modules.system.router import router
from app.modules.trip.router import router as trip_router
from app.modules.pdf.router import router as pdf_router


from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(
    router,
    prefix="/api/v1",
)

app.include_router(
    trip_router,
    prefix="/api/v1/trips",
    tags=["Trips"],
)

app.include_router(
    pdf_router,
    prefix="/api/v1/pdf",
    tags=["PDF"],
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}"
    }