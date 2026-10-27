from app.modules.trip.models import Trip


class PromptBuilder:

    @staticmethod
    def build_trip_prompt(trip: Trip) -> str:

        return f"""
You are an expert travel planner.

Generate a concise, practical travel itinerary. Include exactly {trip.duration_days} days.
For each day, include exactly 3 activities (morning, afternoon, evening). Keep each
activity description to one short sentence and each overview to one sentence. Keep
the entire response compact so it fits within the output limit.

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
  "summary": "2–3 sentence overview of the complete trip",

  "days": [
    {{
      "day": 1,
      "title": "Arrival and Beach Relaxation",
      "overview": "One sentence describing the theme and highlights of the day.",

      "activities": [
        {{
          "time": "09:00",
          "activity": "Relax on Candolim Beach",
          "location": "Candolim Beach, Goa",
          "description": "One concise sentence about the activity.",
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