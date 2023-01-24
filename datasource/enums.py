from django.db import models

from .datasources import Datasource, HeartRate


class Datasources(models.TextChoices):
    HEART_RATE = "heart_rate"

    @property
    def datasource_class(self) -> type[Datasource]:
        return {
            Datasources.HEART_RATE: HeartRate,
        }[self]

    @property
    def db_model(self) -> type[models.Model]:
        from .models import HeartRateData

        return {
            Datasources.HEART_RATE: HeartRateData,
        }[self]

    @property
    def variable_name(self) -> str:
        return {
            Datasources.HEART_RATE: "heart_rate",
        }[self]
