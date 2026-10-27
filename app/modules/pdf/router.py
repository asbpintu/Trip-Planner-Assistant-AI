from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.trip.repository import TripRepository
from app.services.pdf.pdf_service import PDFService

router = APIRouter()


@router.post("/{public_id}")
def generate_pdf(
    public_id: UUID,
    db: Session = Depends(get_db),
):
    repository = TripRepository(db)

    trip = repository.get_by_public_id(public_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    if not trip.itinerary_json:
        raise HTTPException(
            status_code=400,
            detail="Generate itinerary first.",
        )

    pdf_service = PDFService()

    pdf_path = pdf_service.generate_trip_pdf(trip)

    pdf_path = pdf_service.generate_trip_pdf(trip)

    print("Returned filename:", pdf_path.name)

    return {
        "message": "PDF generated successfully.",
        "filename": pdf_path.name,
        "download_url": f"/api/v1/pdf/download/{pdf_path.name}",
    }


@router.get("/download/{filename}")
def download_pdf(filename: str):

    pdf_path = PDFService().output_dir / filename

    print("Looking for:", pdf_path.resolve())
    print("Exists:", pdf_path.exists())

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF not found.",
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=filename,
    )