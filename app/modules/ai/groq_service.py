from groq import Groq

from app.core.config import settings

ITINERARY_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "trip_itinerary",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "days": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "title": {"type": "string"},
                            "overview": {"type": "string"},
                            "activities": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "time": {"type": "string"},
                                        "activity": {"type": "string"},
                                        "location": {"type": "string"},
                                        "description": {"type": "string"},
                                        "estimated_cost": {"type": "string"},
                                    },
                                    "required": [
                                        "time",
                                        "activity",
                                        "location",
                                        "description",
                                        "estimated_cost",
                                    ],
                                    "additionalProperties": False,
                                },
                            },
                        },
                        "required": ["day", "title", "overview", "activities"],
                        "additionalProperties": False,
                    },
                },
                "packing_tips": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "estimated_budget": {"type": "string"},
                "best_time_to_visit": {"type": "string"},
                "important_notes": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "summary",
                "days",
                "packing_tips",
                "estimated_budget",
                "best_time_to_visit",
                "important_notes",
            ],
            "additionalProperties": False,
        },
    },
}


class GroqService:

    def __init__(self):
        self.api_key = (settings.GROQ_API_KEY or "").strip()
        self.client = Groq(api_key=self.api_key)
        fallback_models = [
            model.strip()
            for model in (settings.GROQ_MODEL_FALLBACKS or "").split(",")
            if model.strip()
        ]
        self.models = [
            model
            for model in [settings.GROQ_MODEL.strip(), *fallback_models]
            if model
        ]

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured. Add it to your .env file.")

        last_error = None

        for model in self.models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=0.4,
                    max_completion_tokens=8192,
                    response_format=ITINERARY_RESPONSE_FORMAT,
                )

                content = getattr(response.choices[0].message, "content", "") or ""
                content = content.strip()

                if content.startswith("```json"):
                    content = content.replace("```json", "", 1)

                if content.startswith("```"):
                    content = content.replace("```", "", 1)

                if content.endswith("```"):
                    content = content[:-3]

                return content.strip()

            except Exception as exc:  # pragma: no cover - retries across Groq models
                last_error = exc
                error_name = type(exc).__name__
                if error_name not in {"NotFoundError", "BadRequestError"}:
                    raise

        if last_error is not None:
            raise RuntimeError(
                f"Unable to generate a trip with the configured Groq models "
                f"({', '.join(self.models)}): {last_error}"
            ) from last_error

        raise RuntimeError("No Groq model was configured for itinerary generation.")