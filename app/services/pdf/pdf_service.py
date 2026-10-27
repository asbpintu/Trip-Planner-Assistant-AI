import json
from pathlib import Path

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

        self.normal_style = self.styles["BodyText"]

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
                "🌍 Trip Planner Assistant AI",
                self.title_style,
            )
        )

        story.append(
            Paragraph(
                "<b>AI Generated Travel Itinerary</b>",
                self.styles["Heading2"],
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

        info = f"""
        <b>Title:</b> {trip.title}<br/>
        <b>Destination:</b> {trip.destination}, {trip.destination_country}<br/>
        <b>Duration:</b> {trip.duration_days} Days<br/>
        <b>Travelers:</b> {trip.travelers}<br/>
        <b>Budget:</b> {trip.budget} {trip.currency}<br/>
        <b>Trip Type:</b> {trip.trip_type.title()}<br/>
        """

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
                itinerary.get("summary", ""),
                self.normal_style,
            )
        )

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
                    f"Day {day['day']} - {day['title']}",
                    self.sub_heading_style,
                )
            )

            if day.get("overview"):

                story.append(
                    Paragraph(
                        day["overview"],
                        self.normal_style,
                    )
                )

                story.append(Spacer(1, 8))

            for activity in day.get("activities", []):

                activity_text = f"""
                <b>Time:</b> {activity['time']}<br/>
                <b>Activity:</b> {activity['activity']}<br/>
                <b>Location:</b> {activity['location']}<br/>
                <b>Description:</b><br/>
                {activity['description']}<br/>
                <b>Estimated Cost:</b> {activity['estimated_cost']}
                """

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
                        f"• {item}",
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
                        f"• {note}",
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