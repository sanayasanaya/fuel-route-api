from math import radians, sin, cos, sqrt, atan2

from fuel.models import FuelStation


ROUTE_CORRIDOR_MILES = 25


def calculate_distance_miles(lat1, lon1, lat2, lon2):
    """
    Calculate approximate distance between two coordinates
    using the Haversine formula.
    """

    earth_radius_miles = 3958.8

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_miles * c


def calculate_route_distance_from_start(
    station_lat,
    station_lon,
    route_coordinates,
):
    """
    Calculate the approximate distance from the route start
    to the fuel station.

    This uses the route's coordinate points and finds the
    closest route point to the station.
    """

    closest_index = None
    closest_distance = float("inf")

    for index, point in enumerate(route_coordinates):

        route_lon = point[0]
        route_lat = point[1]

        distance = calculate_distance_miles(
            station_lat,
            station_lon,
            route_lat,
            route_lon,
        )

        if distance < closest_distance:
            closest_distance = distance
            closest_index = index

    if closest_index is None:
        return None

    distance_from_start = 0.0

    for index in range(1, closest_index + 1):

        previous_lon = route_coordinates[index - 1][0]
        previous_lat = route_coordinates[index - 1][1]

        current_lon = route_coordinates[index][0]
        current_lat = route_coordinates[index][1]

        distance_from_start += calculate_distance_miles(
            previous_lat,
            previous_lon,
            current_lat,
            current_lon,
        )

    return distance_from_start


def get_route_stations(route_coordinates):
    """
    Find fuel stations close to the route.

    Returns stations with:

    - station information
    - fuel price
    - distance from route
    - approximate distance from route start
    """

    stations = FuelStation.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False,
        retail_price__isnull=False,
    )

    results = []

    for station in stations:

        station_lat = float(station.latitude)
        station_lon = float(station.longitude)

        minimum_distance = min(
            calculate_distance_miles(
                station_lat,
                station_lon,
                point[1],
                point[0],
            )
            for point in route_coordinates
        )

        if minimum_distance > ROUTE_CORRIDOR_MILES:
            continue

        distance_from_start = (
            calculate_route_distance_from_start(
                station_lat,
                station_lon,
                route_coordinates,
            )
        )

        if distance_from_start is None:
            continue

        results.append(
            {
                "id": station.id,
                "station": station.truckstop_name,
                "address": station.address,
                "city": station.city,
                "state": station.state,
                "latitude": station_lat,
                "longitude": station_lon,
                "price_per_gallon": float(
                    station.retail_price
                ),
                "distance_from_route": round(
                    minimum_distance,
                    2,
                ),
                "distance_from_start": round(
                    distance_from_start,
                    2,
                ),
            }
        )

    results.sort(
        key=lambda station: station["distance_from_start"]
    )

    return results