import csv

from django.core.management.base import BaseCommand

from fuel.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel prices from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        stations = []

        with open(
            csv_file,
            "r",
            encoding="utf-8-sig",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                stations.append(
                    FuelStation(
                        opis_truckstop_id=int(
                            row["OPIS Truckstop ID"]
                        ),
                        truckstop_name=row["Truckstop Name"],
                        address=row["Address"],
                        city=row["City"],
                        state=row["State"],
                        rack_id=int(row["Rack ID"]),
                        retail_price=row["Retail Price"],
                    )
                )

        FuelStation.objects.bulk_create(
            stations,
            batch_size=1000,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(stations)} fuel stations."
            )
        )