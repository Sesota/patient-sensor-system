from typing import TYPE_CHECKING
from django.db import models
from django.db.models.query import QuerySet

from user.validators import UserRoleValidator
from user.enums import Role
from utils.criteria import evaluate_criteria

if TYPE_CHECKING:
    from .enums import Datasources
    from supervision.models import Supervision


class BaseDatasource(models.Model):
    class Meta:
        abstract = True

    criteria_placeholders: dict[str, str]

    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        validators=[UserRoleValidator(Role.PATIENT)],
    )
    device = models.ForeignKey(
        "device.Device",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    record_time = models.DateTimeField()

    @property
    def datasource(self) -> "Datasources":
        from .enums import Datasources

        return next(ds for ds in Datasources if ds.db_model == self.__class__)

    def save(self, *args, **kwargs):
        alerting_supervisions = self.get_alerting_supervisions()
        if alerting_supervisions:
            for supervision in alerting_supervisions:
                supervision.alert(self)

        super().save(*args, **kwargs)

    def get_alerting_supervisions(
        self, supervisions: "QuerySet[Supervision] | None" = None
    ) -> list["Supervision"]:
        from supervision.models import DatasourcesConfig

        alerting_supervisions = []

        if supervisions is None:
            supervisions = self.user.supervisors.all()

        supervisions_with_this_datasource = supervisions.filter(
            id__in=DatasourcesConfig.objects.filter(
                datasource=self.datasource
            ).values_list("supervision_id", flat=True)
        )
        for supervision in supervisions_with_this_datasource:
            should_alert = evaluate_criteria(
                supervision.datasources_configs.get(
                    datasource=self.datasource
                ).alerting_criteria,
                **self.values(),
            )
            if should_alert:
                alerting_supervisions.append(supervision)

        return alerting_supervisions

    def values(self):
        return {
            k: getattr(self, v) for k, v in self.criteria_placeholders.items()
        }


class HeartRateData(BaseDatasource):
    criteria_placeholders = {"hr": "heart_rate"}

    heart_rate = models.IntegerField()


class BloodPressureData(BaseDatasource):
    criteria_placeholders = {"sbp": "systolic_bp", "dbp": "diastolic_bp"}

    systolic_bp = models.IntegerField()
    diastolic_bp = models.IntegerField()
