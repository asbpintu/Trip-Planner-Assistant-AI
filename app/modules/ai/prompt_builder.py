from app.modules.trip.models import Trip


class PromptBuilder:

    @staticmethod
    def build_trip_prompt(trip: Trip) -> str:

        return f"""
You are a professional travel consultant. Create a polished, realistic itinerary tailored
to the trip details below. Prioritize a practical pace, clear logistics, geographic sense,
and useful details over generic recommendations.

Planning requirements:
- Include exactly {trip.duration_days} numbered days and exactly 3 activities per day.
- Schedule one activity in the morning, one in the afternoon, and one in the evening.
- Schedule activities in chronological order, with sensible start times and enough time
  for the experience and travel between locations. Group nearby places to avoid backtracking.
- Make each day overview one concise sentence that explains its theme and flow.
- Write each activity description as 2-3 concise, informative sentences (about 2-3 printed
  lines). Explain what the traveler will do or see and include a useful practical detail
  when relevant, such as a reservation, access, or transit consideration.
- Give each activity a useful location in the format "venue, neighborhood or district,
  city, country". Use specific, recognizable place names. Never invent street addresses,
  opening hours, travel times, or access rules; use a neighborhood and city if an exact
  address is not known.
- Keep recommendations relevant to the trip type, preferences, group size, dates, and
  stated budget. Do not present uncertain prices or logistics as guaranteed facts.
- Use the requested currency for cost estimates and clearly mark them as estimates.
  Keep the overall budget realistic for all travelers and state what it includes.
- Make the overall summary 2-3 professional sentences describing the destination, dates,
  trip pace, and key experiences. Avoid vague promotional language and repeated details.
- Keep packing tips and important notes specific to this destination and itinerary.
- If an operational detail may change (for example, opening hours or availability), advise
  the traveler to confirm it before departure rather than guessing.

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
  "summary": "Professional 2-3 sentence overview of the complete trip",

  "days": [
    {{
      "day": 1,
      "title": "A clear, specific title for the day",
      "overview": "One sentence describing the theme, pace, and highlights of the day.",

      "activities": [
        {{
          "time": "09:00",
          "activity": "A clear name for the scheduled experience",
          "location": "Named venue, neighborhood or district, city, country",
          "description": "2-3 sentences covering the experience and practical tips.",
          "estimated_cost": "Approximate cost in {trip.currency}"
        }}
      ]
    }}
  ],

  "packing_tips": [],
  "estimated_budget": "Approximate total for all travelers in {trip.currency}; state inclusions",
  "best_time_to_visit": "...",
  "important_notes": []
}}
"""