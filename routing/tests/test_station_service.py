from django.test import TestCase

from fuel.models import FuelStation
from routing.services.station_service import (
    calculate_distance_miles,
    get_route_stations,
)


class StationServiceTests(TestCase):

    def setUp(self):
        FuelStation.objects.create(
            opis_truckstop_id=999999,
            truckstop_name="Test Station 1",
            address="123 Test Road",
            city="Test City",
            state="PA",
            rack_id=1,
            retail_price=3.50,
            latitude=40.50,
            longitude=-75.00,
        )

        FuelStation.objects.create(
            opis_truckstop_id=999998,
            truckstop_name="Test Station 2",
            address="456 Test Road",
            city="Test City 2",
            state="PA",
            rack_id=2,
            retail_price=3.20,
            latitude=40.30,
            longitude=-76.00,
        )

    def test_calculate_distance_miles(self):
        distance = calculate_distance_miles(
            40.50,
            -75.00,
            40.50,
            -75.00,
        )

        self.assertEqual(distance, 0)

    def test_get_route_stations(self):
        route_coordinates = [
            [-74.0060, 40.7128],
            [-75.0, 40.5],
            [-76.0, 40.3],
            [-77.0, 40.0],
        ]

        stations = get_route_stations(route_coordinates)

        self.assertEqual(len(stations), 2)

        self.assertEqual(
            stations[0]["station"],
            "Test Station 1",
        )

        self.assertEqual(
            stations[1]["station"],
            "Test Station 2",
        )

    def test_station_distance_from_route(self):
        route_coordinates = [
            [-74.0060, 40.7128],
            [-75.0, 40.5],
            [-76.0, 40.3],
            [-77.0, 40.0],
        ]

        stations = get_route_stations(route_coordinates)

        for station in stations:
            self.assertLessEqual(
                station["distance_from_route"],
                25,
            )

    def test_station_distance_from_start(self):
        route_coordinates = [
            [-74.0060, 40.7128],
            [-75.0, 40.5],
            [-76.0, 40.3],
            [-77.0, 40.0],
        ]

        stations = get_route_stations(route_coordinates)

        self.assertGreater(
            stations[0]["distance_from_start"],
            0,
        )

        self.assertGreater(
            stations[1]["distance_from_start"],
            stations[0]["distance_from_start"],
        )