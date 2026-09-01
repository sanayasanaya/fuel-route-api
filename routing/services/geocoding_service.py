import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_location(location: str) -> dict:
    params = {
        "q": f"{location}, USA",
        "format": "json",
        "limit": 1,
        "countrycodes": "us",
    }

    headers = {
        "User-Agent": "fuel-route-api/1.0"
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(
            f"Could not find location: {location}"
        )

    result = results[0]

    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "display_name": result["display_name"],
    }