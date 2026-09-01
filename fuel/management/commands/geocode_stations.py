import time

import requests
from django.core.management.base import BaseCommand

from fuel.models import FuelStation

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL",
    "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
    "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
    "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
    "VA", "WA", "WV", "WI", "WY",
}


class Command(BaseCommand):
    help = "Geocode fuel stations using city and state"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=5,
            help="Maximum number of stations to geocode",
        )

    def handle(self, *args, **options):
        stations = (
            FuelStation.objects
            .filter(
                latitude__isnull=True,
                longitude__isnull=True,
                state__in=US_STATES,
            )
            .exclude(city__isnull=True)
            .exclude(state__isnull=True)
            .order_by("city", "state")
        ) 

        limit = options["limit"]
        if limit > 0:
            stations = stations[:limit]

        total = stations.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Stations needing coordinates: {total}"
            )
        )

        session = requests.Session()

        session.headers.update({
            "User-Agent": "fuel-route-api/1.0"
        })

        processed_locations = {}

        updated = 0
        failed = 0

        for station in stations:
            city = station.city.strip()
            state = station.state.strip()

            location_key = f"{city}, {state}"

            # Reuse coordinates if this city/state was already processed
            if location_key in processed_locations:
                coordinates = processed_locations[location_key]

                if coordinates:
                    station.latitude = coordinates[0]
                    station.longitude = coordinates[1]
                    station.save(
                        update_fields=["latitude", "longitude"]
                    )
                    updated += 1

                continue

            self.stdout.write(
                f"Geocoding: {location_key}"
            )

            try:
                response = session.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={
                        "q": f"{city}, {state}, USA",
                        "format": "json",
                        "limit": 1,
                        "countrycodes": "us",
                    },
                    timeout=10,
                )

                response.raise_for_status()

                results = response.json()

                if results:
                    latitude = float(results[0]["lat"])
                    longitude = float(results[0]["lon"])

                    coordinates = (latitude, longitude)

                    processed_locations[location_key] = coordinates

                    station.latitude = latitude
                    station.longitude = longitude

                    station.save(
                        update_fields=["latitude", "longitude"]
                    )

                    updated += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Found: {latitude}, {longitude}"
                        )
                    )

                else:
                    processed_locations[location_key] = None

                    failed += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"  Not found: {location_key}"
                        )
                    )

            except requests.RequestException as exc:
                processed_locations[location_key] = None

                failed += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"  Request failed: {exc}"
                    )
                )

            # Respect Nominatim's public usage policy.
            time.sleep(1)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated: {updated}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Failed: {failed}"
            )
        )