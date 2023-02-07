from typing import TYPE_CHECKING
from django.db import models

from datasource.models import BloodPressureData, HeartRateData
from utils.enums import ClassEnumMixin

if TYPE_CHECKING:
    from .models import BaseDatasource


class Datasource:
    db_model: type["BaseDatasource"]
    variable_names: list[str]


class HeartRate(Datasource):
    db_model = HeartRateData
    variable_names = ["heart_rate"]


class BloodPressure(Datasource):
    db_model = BloodPressureData
    variable_names = ["systolic_bp", "diastolic_bp"]


class Datasources(ClassEnumMixin, models.TextChoices):
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE = "blood_pressure"

    @property
    def klass(self) -> type["Datasource"]:
        return {
            object.__getattribute__(self, "HEART_RATE"): HeartRate,
            object.__getattribute__(self, "BLOOD_PRESSURE"): BloodPressure,
        }[self]
