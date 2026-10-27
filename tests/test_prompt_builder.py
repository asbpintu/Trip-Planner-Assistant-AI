from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.modules.ai.prompt_builder import PromptBuilder


def test_trip_prompt_requests_detailed_and_grounded_activity_plans():
    trip = SimpleNamespace(
        duration_days=2,
        destination="Kyoto",
        destination_country="Japan",
        title="Kyoto Culture Trip",
        start_date=date(2026, 11, 1),
        end_date=date(2026, 11, 2),
        travelers=2,
        budget=Decimal("1200.00"),
        currency="USD",
        trip_type="Cultural",
        preferences="Temples and local food",
        description="A relaxed first visit.",
    )

    prompt = PromptBuilder.build_trip_prompt(trip)

    assert "exactly 2 numbered days and exactly 3 activities per day" in prompt
    assert "one activity in the morning, one in the afternoon, and one in the evening" in prompt
    assert "2-3 concise, informative sentences" in prompt
    assert "what the specific place is known for" in prompt
    assert "why it attracts visitors" in prompt
    assert "3-4 professional, concise sentences" in prompt
    assert "venue, neighborhood or district, city, country" in prompt
    assert "Never invent street addresses" in prompt
    assert "Approximate cost in USD" in prompt
