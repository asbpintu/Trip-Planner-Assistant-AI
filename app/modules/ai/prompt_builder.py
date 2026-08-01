from app.modules.trip.models import Trip


class PromptBuilder:

    @staticmethod
    def build_trip_prompt(trip: Trip) -> str:

        return f"""
You are an expert travel planner.

Generate a detailed travel itinerary.

Destination:
{trip.destination}

Country:
{trip.destination_country}

Trip Title:
{trip.title}

Travel Dates:
{trip.start_date} to {trip.end_date}

Duration:
{trip.duration_days} days

Travelers:
{trip.travelers}

Budget:
{trip.budget} {trip.currency}

Trip Type:
{trip.trip_type}

Preferences:
{trip.preferences}

Description:
{trip.description}

Return ONLY valid JSON.

The JSON format should be:

{{
  "summary": "5–6 line overview of the complete trip",

  "days": [
    {{
      "day": 1,
      "title": "Arrival and Beach Relaxation",
      "overview": "2–3 lines describing the theme and highlights of the day.",

      "activities": [
        {{
          "time": "09:00",
          "activity": "Relax on Candolim Beach",
          "location": "Candolim Beach, Goa",
          "description": "2–4 lines explaining why this place is famous and what visitors can enjoy.",
          "estimated_cost": "0 USD"
        }}
      ]
    }}
  ],

  "packing_tips": [],
  "estimated_budget": "...",
  "best_time_to_visit": "...",
  "important_notes": []
}}
"""