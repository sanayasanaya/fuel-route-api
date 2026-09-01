MAX_RANGE_MILES = 500

FUEL_EFFICIENCY_MPG = 10

MAX_FUEL_GALLONS = (
    MAX_RANGE_MILES / FUEL_EFFICIENCY_MPG
)


def calculate_fuel_required(distance_miles):
    """
    Calculate fuel required for a given distance.
    """
    return distance_miles / FUEL_EFFICIENCY_MPG


def is_reachable(distance_miles):
    """
    Check whether a distance can be travelled
    within the vehicle's maximum range.
    """
    return distance_miles <= MAX_RANGE_MILES


def calculate_fuel_cost(fuel_gallons, price_per_gallon):
    """
    Calculate the cost of fuel.
    """
    return fuel_gallons * price_per_gallon


def optimize_fuel_stops(stations, route_distance_miles):
    """
    Select cost-effective fuel stops while respecting
    the vehicle's 500-mile maximum range.

    stations must be ordered along the route.

    Each station should contain:
        - distance_from_start
        - price_per_gallon
        - station information

    Returns a list of recommended fuel stops.
    """

    if route_distance_miles <= 0:
        return []

    if route_distance_miles <= MAX_RANGE_MILES:
        return []

    if not stations:
        raise ValueError(
            "No fuel stations are available along the route."
        )

    # Remove stations that are outside the route
    # and sort them by their distance from the start.
    valid_stations = sorted(
        [
            station
            for station in stations
            if 0 < station["distance_from_start"] < route_distance_miles
        ],
        key=lambda station: station["distance_from_start"],
    )

    # Add destination as the final point.
    points = valid_stations + [
        {
            "distance_from_start": route_distance_miles,
            "is_destination": True,
        }
    ]

    selected_stops = []

    current_position = 0.0
    current_fuel = MAX_FUEL_GALLONS

    station_index = 0

    while current_position < route_distance_miles:

        # Find stations reachable from current position.
        reachable = []

        for index in range(station_index, len(valid_stations)):
            station = valid_stations[index]

            distance_to_station = (
                station["distance_from_start"]
                - current_position
            )

            if distance_to_station <= MAX_RANGE_MILES:
                reachable.append((index, station))
            else:
                break

        # Check whether destination itself is reachable.
        distance_to_destination = (
            route_distance_miles - current_position
        )

        if distance_to_destination <= MAX_RANGE_MILES:
            break

        if not reachable:
            raise ValueError(
                "No feasible fuel station within 500 miles."
            )

        # Current station price, if we are already at a station.
        current_price = None

        if selected_stops:
            current_price = selected_stops[-1]["price_per_gallon"]

        # Find the cheapest reachable station.
        cheapest_index, cheapest_station = min(
            reachable,
            key=lambda item: item[1]["price_per_gallon"],
        )

        # Distance to cheapest reachable station.
        distance_to_cheapest = (
            cheapest_station["distance_from_start"]
            - current_position
        )

        fuel_needed = calculate_fuel_required(
            distance_to_cheapest
        )

        # Consume fuel needed to reach the cheapest station.
        current_fuel -= fuel_needed

        # We need to decide how much fuel to buy.
        fuel_to_buy = 0.0

        # Look for a cheaper station before the cheapest
        # reachable station.
        cheaper_station = None

        for index, station in reachable:
            if (
                station["price_per_gallon"]
                < cheapest_station["price_per_gallon"]
            ):
                cheaper_station = station
                break

        if cheaper_station:
            target_distance = (
                cheaper_station["distance_from_start"]
                - current_position
            )

            required_fuel = calculate_fuel_required(
                target_distance
            )

            fuel_to_buy = max(
                0.0,
                required_fuel - current_fuel,
            )

        else:
            # No cheaper station within reach.
            # Fill the tank enough to maximize range.
            fuel_to_buy = max(
                0.0,
                MAX_FUEL_GALLONS - current_fuel,
            )

        fuel_to_buy = min(
            fuel_to_buy,
            MAX_FUEL_GALLONS - current_fuel,
        )

        # If we are not actually at the cheapest station yet,
        # move to it first.
        current_position = cheapest_station[
            "distance_from_start"
        ]

        current_fuel = max(
            0.0,
            current_fuel,
        )

        # Buy fuel at this station.
        current_fuel += fuel_to_buy

        fuel_cost = calculate_fuel_cost(
            fuel_to_buy,
            cheapest_station["price_per_gallon"],
        )

        selected_stops.append(
            {
                **cheapest_station,
                "fuel_added_gallons": round(
                    fuel_to_buy,
                    2,
                ),
                "fuel_cost": round(
                    fuel_cost,
                    2,
                ),
            }
        )

        station_index = cheapest_index + 1

    return selected_stops


def calculate_total_fuel_cost(fuel_stops):
    """
    Calculate total fuel cost for selected stops.
    """
    return round(
        sum(
            stop["fuel_cost"]
            for stop in fuel_stops
        ),
        2,
    )


def calculate_total_fuel(fuel_stops):
    """
    Calculate total gallons purchased.
    """
    return round(
        sum(
            stop["fuel_added_gallons"]
            for stop in fuel_stops
        ),
        2,
    )