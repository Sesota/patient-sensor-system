from datetime import datetime
from typing import Any, Literal
from django.db import models

from ninja import Schema

from datasource.enums import Datasources


class DatasourceUpload(Schema):
    datasource: Datasources

    def create(self, **kwargs) -> models.Model:
        db_model = self.datasource.db_model
        fields = self.dict()
        fields.pop("datasource")

        return db_model.objects.create(**kwargs, **fields)

class HeartRateUpload(DatasourceUpload):
    datasource: Literal[Datasources.HEART_RATE]
    heart_rate: int
    record_time: datetime

