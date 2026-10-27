import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.modules.trip.models import Trip


class PDFService:

    def __init__(self):

        self.output_dir = Path("generated/pdfs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print("PDF Output Directory:", self.output_dir)

        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "TitleStyle",
            parent=self.styles["Title"],
            alignment=TA_CENTER,
            fontSize=24,
            textColor=HexColor("#0E7490"),
            spaceAfter=20,
        )

        self.subtitle_style = ParagraphStyle(
            "SubtitleStyle",
            parent=self.styles["Heading2"],
            alignment=TA_CENTER,
            textColor=HexColor("#334155"),
            spaceAfter=8,
        )

        self.heading_style = ParagraphStyle(
            "HeadingStyle",
            parent=self.styles["Heading2"],
            textColor=HexColor("#0E7490"),
            spaceBefore=15,
            spaceAfter=10,
        )

        self.sub_heading_style = ParagraphStyle(
            "SubHeading",
            parent=self.styles["Heading3"],
            textColor=HexColor("#1E3A8A"),
            spaceBefore=10,
            spaceAfter=5,
        )

        self.activity_style = ParagraphStyle(
            "ActivityStyle",
            parent=self.styles["Heading3"],
            textColor=HexColor("#1E3A8A"),
            spaceBefore=5,
            spaceAfter=4,
        )

        self.normal_style = ParagraphStyle(
            "BodyTextStyle",
            parent=self.styles["BodyText"],
            leading=14,
        )

    @staticmethod
    def _safe_text(value: object) -> str:
        return escape(str(value if value is not None else "")).replace("\n", "<br/>")

    def generate_trip_pdf(self, trip: Trip) -> Path:

        filepath = self.output_dir / f"{trip.public_id}.pdf"

        itinerary = json.loads(trip.itinerary_json or "{}")

        document = SimpleDocTemplate(
            str(filepath),
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch,
        )

        story = []

        # --------------------------------------------------------
        # Title
        # --------------------------------------------------------

        story.append(
            Paragraph(
                "Trip Planner Assistant AI",
                self.title_style,
            )
        )

        story.append(
            Paragraph(
                "Personalized Travel Itinerary",
                self.subtitle_style,
            )
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------------
        # Trip Information
        # --------------------------------------------------------

        story.append(
            Paragraph(
                "Trip Information",
                self.heading_style,
            )
        )

        info = "<br/>".join(
            [
                f"<b>Title:</b> {self._safe_text(trip.title)}",
                f"<b>Destination:</b> {self._safe_text(trip.destination)}, "
                f"{self._safe_text(trip.destination_country)}",
                f"<b>Travel dates:</b> {self._safe_text(trip.start_date)} to "
                f"{self._safe_text(trip.end_date)}",
                f"<b>Duration:</b> {self._safe_text(trip.duration_days)} days",
                f"<b>Travelers:</b> {self._safe_text(trip.travelers)}",
                f"<b>Budget:</b> {self._safe_text(trip.budget)} "
                f"{self._safe_text(trip.currency)}",
                f"<b>Trip type:</b> "
                f"{self._safe_text(trip.trip_type.title())}",
            ]
        )

        story.append(
            Paragraph(
                info,
                self.normal_style,
            )
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------------
        # Summary
        # --------------------------------------------------------

        story.append(
            Paragraph(
                "Trip Summary",
                self.heading_style,
            )
        )

        story.append(
            Paragraph(
                self._safe_text(itinerary.get("summary", "")),
                self.normal_style,
            )
        )

        planning_details = []
        if itinerary.get("estimated_budget"):
            planning_details.append(
                f"<b>Estimated trip budget:</b> "
                f"{self._safe_text(itinerary['estimated_budget'])}"
            )
        if itinerary.get("best_time_to_visit"):
            planning_details.append(
                f"<b>Best time to visit:</b> "
                f"{self._safe_text(itinerary['best_time_to_visit'])}"
            )

        if planning_details:
            story.append(Spacer(1, 8))
            story.append(Paragraph("<br/>".join(planning_details), self.normal_style))

        story.append(Spacer(1, 20))

        # --------------------------------------------------------
        # Daily Itinerary
        # --------------------------------------------------------

        story.append(
            Paragraph(
                "Daily Itinerary",
                self.heading_style,
            )
        )

        for day in itinerary.get("days", []):

            story.append(
                Paragraph(
                    f"Day {self._safe_text(day.get('day', ''))} - "
                    f"{self._safe_text(day.get('title', ''))}",
                    self.sub_heading_style,
                )
            )

            if day.get("overview"):

                story.append(
                    Paragraph(
                        self._safe_text(day["overview"]),
                        self.normal_style,
                    )
                )

                story.append(Spacer(1, 8))

            for index, activity in enumerate(day.get("activities", []), start=1):

                story.append(
                    Paragraph(
                        f"{index}. {self._safe_text(activity.get('time', ''))} "
                        f"- {self._safe_text(activity.get('activity', ''))}",
                        self.activity_style,
                    )
                )

                activity_text = (
                    f"<b>Location:</b> "
                    f"{self._safe_text(activity.get('location', ''))}<br/>"
                    f"<b>Details:</b> "
                    f"{self._safe_text(activity.get('description', ''))}<br/>"
                    f"<b>Estimated cost:</b> "
                    f"{self._safe_text(activity.get('estimated_cost', ''))}"
                )

                story.append(
                    Paragraph(
                        activity_text,
                        self.normal_style,
                    )
                )

                story.append(Spacer(1, 12))

            story.append(Spacer(1, 15))

        # --------------------------------------------------------
        # Packing Tips
        # --------------------------------------------------------

        packing = itinerary.get("packing_tips", [])

        if packing:

            story.append(
                Paragraph(
                    "Packing Tips",
                    self.heading_style,
                )
            )

            for item in packing:

                story.append(
                    Paragraph(
                        f"• {self._safe_text(item)}",
                        self.normal_style,
                    )
                )

            story.append(Spacer(1, 15))

        # --------------------------------------------------------
        # Important Notes
        # --------------------------------------------------------

        notes = itinerary.get("important_notes", [])

        if notes:

            story.append(
                Paragraph(
                    "Important Notes",
                    self.heading_style,
                )
            )

            for note in notes:

                story.append(
                    Paragraph(
                        f"• {self._safe_text(note)}",
                        self.normal_style,
                    )
                )

            story.append(Spacer(1, 20))

        # --------------------------------------------------------
        # Footer
        # --------------------------------------------------------

        story.append(
            Paragraph(
                "<br/><br/><b>Generated by Trip Planner Assistant AI</b>",
                self.styles["Italic"],
            )
        )

        print(filepath)
        document.build(story)
        print("Saved:", filepath)
        print("Exists:", filepath.exists())

        return filepath