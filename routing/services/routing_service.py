import requests


OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(
    start_latitude: float,
    start_longitude: float,
    finish_latitude: float,
    finish_longitude: float,
) -> dict:

    coordinates = (
        f"{start_longitude},{start_latitude};"
        f"{finish_longitude},{finish_latitude}"
    )

    url = f"{OSRM_URL}/{coordinates}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
        "alternatives": "false",
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError(
            f"Routing failed: {data.get('code')}"
        )

    route = data["routes"][0]

    return {
        "distance_miles": round(
            route["distance"] / 1609.344,
            2,
        ),
        "duration_minutes": round(
            route["duration"] / 60,
            2,
        ),
        "geometry": route["geometry"],
    }