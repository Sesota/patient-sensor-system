from django.db import models

from .enums import Datasources
from supervision.models import Supervision
from user.validators import UserRoleValidator
from user.enums import Role
from utils.criteria import evaluate_criteria


class HeartRateData(models.Model):
    datasource = Datasources.HEART_RATE

    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="heart_rate_data",
        validators=[UserRoleValidator(Role.PATIENT)],
    )
    device = models.ForeignKey(
        "device.Device",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="heart_rate_data",
    )
    record_time = models.DateTimeField()
    # TODO ^ wish we could have the above fields in an interface class

    heart_rate = models.IntegerField()

    def save(self, *args, **kwargs):
        # TODO maybe move to supervision?
        supervision: Supervision
        for supervision in self.user.supervisors.all():
            should_alert = evaluate_criteria(
                supervision.datasources_configs.get(
                    datasource=self.datasource
                ).alerting_criteria,
                var=self.heart_rate,
            )
            if should_alert:
                ...
        super().save(*args, **kwargs)
