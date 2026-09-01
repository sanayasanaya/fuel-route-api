from django.core.management.base import BaseCommand
from fuel.models import FuelStation


class Command(BaseCommand):
    help = "Clean whitespace from fuel station text fields"

    def handle(self, *args, **options):
        stations = FuelStation.objects.all()

        updated = 0

        for station in stations:
            changed = False

            for field in [
                "truckstop_name",
                "address",
                "city",
                "state",
            ]:
                value = getattr(station, field)

                if value:
                    cleaned = value.strip()

                    if cleaned != value:
                        setattr(station, field, cleaned)
                        changed = True

            if changed:
                station.save(
                    update_fields=[
                        "truckstop_name",
                        "address",
                        "city",
                        "state",
                    ]
                )

                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Cleaned {updated} fuel station records."
            )
        )