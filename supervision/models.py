from typing import TYPE_CHECKING
from django.conf import settings

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models

from datasource.enums import Datasources
from user.enums import Role
from user.validators import UserRoleValidator
from utils.criteria import evaluate_criteria

from .enums import AlertingMedium

if TYPE_CHECKING:
    from datasource.models import BaseDatasource


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

    def alert(self, record: "BaseDatasource"):
        config = DatasourcesConfig.objects.get(
            supervision=self, datasource=record.datasource
        )
        message = (
            f"Patient {self.patient} is in danger.\nA new"
            f" {record.datasource} record has been collected at"
            f" {record.record_time} from this user that has"
            f" {config.alerting_criteria}, {record.values()} and you have"
            " configured your supervision to receive an alert via"
            f" {config.alerting_medium}."
        )
        if config.alerting_medium == AlertingMedium.EMAIL:
            self.send_email(message)
        if config.alerting_medium == AlertingMedium.SMS:
            self.send_sms(message)

    def send_email(self, message: str):
        print(
            f"Sending email to {self.supervisor.email} with message: {message}"
        )
        subject = "[ALERT] Your patient is in danger"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.supervisor.email]
        send_mail(subject, message, email_from, recipient_list)

    def send_sms(self, message):
        pass


supported_variables = ", ".join(
    [
        f"\"{k}\" for \"{v.replace('_', ' ')}\""
        for ds in Datasources
        for k, v in ds.db_model.criteria_placeholders.items()
    ]
)


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
        default="0",
        help_text=(
            "Alerting criteria for this datasource. Supported variables:"
            f" {supported_variables}"
        ),
    )

    @property
    def datasource_model(self) -> type["BaseDatasource"]:
        return Datasources(self.datasource).db_model

    def clean(self):
        # alerting criteria
        if self.alerting_criteria:
            try:
                evaluate_criteria(
                    self.alerting_criteria,
                    **{
                        k: 1
                        for k in self.datasource_model.criteria_placeholders
                    },
                )
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
