import requests

from config import API_BASE_URL


class TripAPI:

    @staticmethod
    def create_trip(data: dict):

        response = requests.post(
            f"{API_BASE_URL}/trips",
            json=data,
            timeout=120,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def generate_itinerary(public_id: str):

        response = requests.post(
            f"{API_BASE_URL}/trips/{public_id}/generate",
            timeout=300,
        )

        response.raise_for_status()

        return response.json()