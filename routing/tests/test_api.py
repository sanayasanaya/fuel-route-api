from unittest.mock import patch

from django.test import TestCase

from fuel.models import FuelStation


class OptimizeRouteAPITests(TestCase):

    def setUp(self):
        self.station = FuelStation.objects.create(
            opis_truckstop_id=999999,
            truckstop_name="Test Fuel Station 1",
            address="123 Test Road",
            city="Test City",
            state="PA",
            rack_id=1,
            retail_price=3.50,
            latitude=40.50,
            longitude=-75.00,
        )

        self.station2 = FuelStation.objects.create(
            opis_truckstop_id=999998,
            truckstop_name="Test Fuel Station 2",
            address="456 Test Road",
            city="Test City 2",
            state="PA",
            rack_id=2,
            retail_price=3.20,
            latitude=40.30,
            longitude=-76.00,
        )

    @patch("routing.views.get_route_stations")
    @patch("routing.views.get_route")
    @patch("routing.views.geocode_location")
    def test_optimize_route_success(
        self,
        mock_geocode,
        mock_get_route,
        mock_get_route_stations,
    ):
        mock_geocode.side_effect = [
            {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "display_name": "New York, NY",
            },
            {
                "latitude": 41.8781,
                "longitude": -87.6298,
                "display_name": "Chicago, IL",
            },
        ]

        mock_get_route.return_value = {
            "distance_miles": 790.0,
            "duration_minutes": 720.0,
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-74.0060, 40.7128],
                    [-75.0, 40.5],
                    [-76.0, 40.3],
                    [-77.0, 40.0],
                ],
            },
        }

        mock_get_route_stations.return_value = [
            {
                "id": 1,
                "station": "Test Fuel Station 1",
                "address": "123 Test Road",
                "city": "Test City",
                "state": "PA",
                "latitude": 40.50,
                "longitude": -75.00,
                "price_per_gallon": 3.50,
                "distance_from_route": 0.0,
                "distance_from_start": 300.0,
            },
            {
                "id": 2,
                "station": "Test Fuel Station 2",
                "address": "456 Test Road",
                "city": "Test City 2",
                "state": "PA",
                "latitude": 40.30,
                "longitude": -76.00,
                "price_per_gallon": 3.20,
                "distance_from_route": 0.0,
                "distance_from_start": 600.0,
            },
        ]

        response = self.client.post(
            "/api/v1/routes/optimize/",
            {
                "start": "New York, NY",
                "finish": "Chicago, IL",
            },
            format="json",
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.data)

        self.assertEqual(response.status_code, 200)

        self.assertIn("start", response.data)
        self.assertIn("finish", response.data)
        self.assertIn("route", response.data)
        self.assertIn("fuel_stops", response.data)
        self.assertIn("total_fuel_gallons", response.data)
        self.assertIn("total_fuel_cost", response.data)

    def test_invalid_request(self):
        response = self.client.post(
            "/api/v1/routes/optimize/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, 400)