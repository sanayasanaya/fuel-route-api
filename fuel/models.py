from django.db import models


class FuelStation(models.Model):
    opis_truckstop_id = models.IntegerField()

    truckstop_name = models.CharField(
        max_length=255
    )

    address = models.CharField(
        max_length=500,
        blank=True
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=2
    )

    rack_id = models.IntegerField()

    retail_price = models.DecimalField(
        max_digits=6,
        decimal_places=3
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["state"]),
            models.Index(fields=["city"]),
            models.Index(fields=["retail_price"]),
        ]

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"