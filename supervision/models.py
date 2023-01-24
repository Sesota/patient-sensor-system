from django.db import models
from django.core.exceptions import ValidationError

from .enums import AlertingMedium
from datasource.enums import Datasources
from user.validators import UserRoleValidator
from user.enums import Role
from utils.criteria import evaluate_criteria


class Supervision(models.Model):
    class Meta:
        unique_together = ["supervisor", "patient"]

    supervisor = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="supervisees",
        validators=[UserRoleValidator(Role.SUPERVISOR)],
    )
    patient = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="supervisors",
        validators=[UserRoleValidator(Role.PATIENT)],
    )

    def __str__(self):
        return f"{self.supervisor} supervising {self.patient}"


class DatasourcesConfig(models.Model):
    class Meta:
        unique_together = ["supervision", "datasource"]

    supervision = models.ForeignKey(
        Supervision,
        on_delete=models.CASCADE,
        related_name="datasources_configs",
    )
    datasource = models.CharField(max_length=127, choices=Datasources.choices)
    alerting_medium = models.CharField(
        max_length=31,
        choices=AlertingMedium.choices,
        default=AlertingMedium.OFF,
        help_text="Alerting medium for this datasource",
    )
    alerting_criteria = models.CharField(
        max_length=255,
        blank=True,
        default='0',
        help_text="Alerting criteria for this datasource",
    )

    def clean(self):
        # alerting criteria
        if self.alerting_criteria:
            try:
                evaluate_criteria(self.alerting_criteria, var=1)
            except Exception:
                raise ValidationError(
                    "Syntax error on alerting criteria when tested with var=1"
                )

        # alerting medium
        if (
            self.alerting_medium == AlertingMedium.EMAIL
            and not self.supervision.supervisor.email
        ):
            raise ValidationError(
                "Supervisor must have specified an email to enable email"
                " alerting"
            )
        elif (
            self.alerting_medium == AlertingMedium.SMS
            and not self.supervision.supervisor.phone_number
        ):
            raise ValidationError(
                "Supervisor must have specified a phone number to enable SMS"
                " alerting"
            )
        super().clean()
