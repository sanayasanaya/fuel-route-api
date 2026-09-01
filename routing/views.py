from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import RouteRequestSerializer
from .services.geocoding_service import geocode_location
from .services.routing_service import get_route
from .services.station_service import get_route_stations
from .services.fuel_optimizer import (
    optimize_fuel_stops,
    calculate_total_fuel,
    calculate_total_fuel_cost,
)

class OptimizeRouteView(APIView):

    def post(self, request):
        serializer = RouteRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        start = serializer.validated_data["start"]
        finish = serializer.validated_data["finish"]

        try:
            start_location = geocode_location(start)
            finish_location = geocode_location(finish)

            route = get_route(
                start_location["latitude"],
                start_location["longitude"],
                finish_location["latitude"],
                finish_location["longitude"],
            )

            route_stations = get_route_stations(
                route["geometry"]["coordinates"]
            )
            fuel_stops = optimize_fuel_stops(
                route_stations,
                route["distance_miles"],
            )
            total_fuel = calculate_total_fuel(
                fuel_stops
            )

            total_fuel_cost = calculate_total_fuel_cost(
                fuel_stops
            )

        except ValueError as exc:
            return Response(
                {
                    "error": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except requests.RequestException:
            return Response(
                {
                    "error": "External service unavailable."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "start": start_location,
                "finish": finish_location,
                "route": route,
                "fuel_stops": fuel_stops,
                "total_fuel_gallons": total_fuel,
                "total_fuel_cost": total_fuel_cost,
            },
            status=status.HTTP_200_OK,
        )