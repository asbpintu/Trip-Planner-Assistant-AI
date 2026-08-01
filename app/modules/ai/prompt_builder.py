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
  "summary": "...",
  "estimated_budget": "...",
  "best_time_to_visit": "...",
  "packing_tips": [
    ...
  ],
  "important_notes": [
    ...
  ],
  "days": [
    {{
      "day": 1,
      "title": "...",
      "activities": [
        {{
          "time": "09:00",
          "activity": "...",
          "location": "...",
          "estimated_cost": "..."
        }}
      ]
    }}
  ]
}}
"""