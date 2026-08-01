import json

import streamlit as st

from api import TripAPI
from ui import header, page_config


page_config()
header()

# -------------------------------
# Trip Creation Form
# -------------------------------

with st.form("trip_form"):

    st.subheader("✈️ Plan Your Trip")

    title = st.text_input(
        "Trip Title",
        placeholder="5 Day Trip to Goa",
    )

    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input(
            "Destination",
            placeholder="Goa",
        )

    with col2:
        country = st.text_input(
            "Country",
            placeholder="India",
        )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    col1, col2, col3 = st.columns(3)

    with col1:
        duration = st.number_input(
            "Duration (Days)",
            min_value=1,
            value=5,
        )

    with col2:
        travelers = st.number_input(
            "Travelers",
            min_value=1,
            value=2,
        )

    with col3:
        budget = st.number_input(
            "Budget",
            min_value=0.0,
            value=500.0,
        )

    col1, col2 = st.columns(2)

    with col1:
        currency = st.selectbox(
            "Currency",
            [
                "USD",
                "INR",
                "EUR",
            ],
        )

    with col2:
        trip_type = st.selectbox(
            "Trip Type",
            [
                "Vacation",
                "Adventure",
                "Business",
                "Family",
                "Honeymoon",
                "Solo",
            ],
        )

    preferences = st.text_area(
        "Preferences",
        placeholder="Beach, Nightlife, Water Sports...",
    )

    description = st.text_area(
        "Description",
        placeholder="Describe your trip...",
    )

    submitted = st.form_submit_button(
        "🚀 Generate AI Itinerary",
        use_container_width=True,
    )

# -------------------------------
# Generate Trip
# -------------------------------

if submitted:

    payload = {
        "title": title,
        "destination": destination,
        "destination_country": country,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "duration_days": duration,
        "travelers": travelers,
        "budget": budget,
        "currency": currency,
        "trip_type": trip_type,
        "preferences": preferences,
        "description": description,
    }

    try:

        with st.spinner("Creating trip..."):

            trip = TripAPI.create_trip(payload)

        with st.spinner("Generating itinerary using AI..."):

            result = TripAPI.generate_itinerary(
                trip["public_id"]
            )

        st.session_state["trip"] = result

        st.success("🎉 AI itinerary generated successfully!")

    except Exception as ex:

        st.error(ex)

# -------------------------------
# Display Generated Trip
# -------------------------------

if "trip" in st.session_state:

    trip = st.session_state["trip"]

    itinerary = json.loads(trip["itinerary_json"])

    st.divider()

    st.header(trip["title"])

    st.caption(
        f"📍 {trip['destination'].title()}, {trip['destination_country'].title()}"
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Duration", f"{trip['duration_days']} Days")
    col2.metric("👥 Travelers", trip["travelers"])
    col3.metric("💰 Budget", f"{trip['budget']} {trip['currency']}")
    col4.metric("🚦 Status", trip["status"])

    st.divider()

    st.subheader("📄 Trip Summary")

    st.write(
        itinerary.get(
            "summary",
            "No summary available.",
        )
    )

    # -------------------------------
    # Daily Itinerary
    # -------------------------------

    st.divider()

    st.subheader("🗓 Daily Itinerary")

    for day in itinerary.get("days", []):

        with st.expander(
            f"Day {day.get('day')} - {day.get('title')}",
            expanded=(day.get("day") == 1),
        ):

            activities = day.get("activities", [])

            if not activities:
                st.info("No activities available.")
                continue

            for activity in activities:

                if isinstance(activity, dict):

                    st.markdown(
                        f"""
### 🕒 {activity.get("time", "")}

**Activity**

{activity.get("activity", "")}

**📍 Location**

{activity.get("location", "")}

**📝 Description**

{activity.get("description", "")}

**💰 Estimated Cost**

{activity.get("estimated_cost", "")}
"""
                    )

                    st.divider()

                else:

                    st.write(f"• {activity}")

    # -------------------------------
    # Packing Tips
    # -------------------------------

    if itinerary.get("packing_tips"):

        st.divider()

        st.subheader("🎒 Packing Tips")

        for item in itinerary["packing_tips"]:

            st.success(item)

    # -------------------------------
    # Important Notes
    # -------------------------------

    if itinerary.get("important_notes"):

        st.divider()

        st.subheader("⚠️ Important Notes")

        for note in itinerary["important_notes"]:

            st.warning(note)