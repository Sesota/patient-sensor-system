from enum import Enum

from .datasources import Datasource, HeartRate


class Datasources(str, Enum):
    HEART_RATE = "heart_rate"

    def datasource_class(self) -> Datasource:
        return {
            Datasources.HEART_RATE: HeartRate,
        }[self]
