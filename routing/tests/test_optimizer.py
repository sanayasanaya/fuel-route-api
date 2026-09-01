from django.test import SimpleTestCase

# from routing.services.fuel_optimizer import (
#     calculate_fuel_required,
#     calculate_fuel_cost,
#     is_reachable,
# )


# class FuelOptimizerTests(SimpleTestCase):

#     def test_calculate_fuel_required(self):
#         result = calculate_fuel_required(100)

#         self.assertEqual(result, 10)

#     def test_is_reachable_500_miles(self):
#         self.assertTrue(is_reachable(500))

#     def test_is_reachable_over_500_miles(self):
#         self.assertFalse(is_reachable(501))

#     def test_calculate_fuel_cost(self):
#         result = calculate_fuel_cost(40, 3.10)

#         self.assertEqual(result, 124)


from django.test import SimpleTestCase

from routing.services.fuel_optimizer import (
    calculate_fuel_required,
    calculate_fuel_cost,
    is_reachable,
    optimize_fuel_stops,
    calculate_total_fuel,
    calculate_total_fuel_cost,
)


class FuelOptimizerTests(SimpleTestCase):

    def test_calculate_fuel_required(self):
        result = calculate_fuel_required(100)

        self.assertEqual(result, 10)

    def test_is_reachable_500_miles(self):
        self.assertTrue(is_reachable(500))

    def test_is_reachable_over_500_miles(self):
        self.assertFalse(is_reachable(501))

    def test_calculate_fuel_cost(self):
        result = calculate_fuel_cost(40, 3.10)

        self.assertEqual(result, 124)

    def test_no_stop_needed_under_500_miles(self):
        stations = [
            {
                "distance_from_start": 200,
                "price_per_gallon": 3.20,
            }
        ]

        result = optimize_fuel_stops(
            stations,
            400,
        )

        self.assertEqual(result, [])

    def test_fuel_stop_needed_over_500_miles(self):
        stations = [
            {
                "id": 1,
                "station": "Station A",
                "distance_from_start": 300,
                "price_per_gallon": 3.50,
            }
        ]

        result = optimize_fuel_stops(
            stations,
            790,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    def test_no_feasible_station(self):
        stations = [
            {
                "id": 1,
                "station": "Station A",
                "distance_from_start": 600,
                "price_per_gallon": 3.50,
            }
        ]

        with self.assertRaises(ValueError):
            optimize_fuel_stops(
                stations,
                790,
            )

    def test_total_fuel(self):
        fuel_stops = [
            {"fuel_added_gallons": 30.0, "fuel_cost": 105.0},
            {"fuel_added_gallons": 20.0, "fuel_cost": 70.0},
        ]

        self.assertEqual(
            calculate_total_fuel(fuel_stops),
            50.0,
        )

    def test_total_fuel_cost(self):
        fuel_stops = [
            {"fuel_added_gallons": 30.0, "fuel_cost": 105.0},
            {"fuel_added_gallons": 20.0, "fuel_cost": 70.0},
        ]

        self.assertEqual(
            calculate_total_fuel_cost(fuel_stops),
            175.0,
        )