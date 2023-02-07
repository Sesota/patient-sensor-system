from datetime import datetime
from typing import Literal

from ninja import Schema

from datasource.enums import Datasources
from datasource.models import BaseDatasource


class DatasourceUpload(Schema):
    datasource: Datasources
    record_time: datetime

    def create(self, **kwargs) -> BaseDatasource:
        db_model = self.datasource.db_model
        fields = self.dict()
        fields.pop("datasource")

        return db_model.objects.create(**kwargs, **fields)


class HeartRateUpload(DatasourceUpload):
    datasource: Literal[Datasources.HEART_RATE]
    heart_rate: int


class BloodPressureUpload(DatasourceUpload):
    datasource: Literal[Datasources.BLOOD_PRESSURE]
    systolic_bp: int
    diastolic_bp: int
