from django.db import models

from .enums import Datasources
from user.validators import UserRoleValidator
from user.enums import Role


class HeartRateData(models.Model):
    datasource = Datasources.HEART_RATE

    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="heart_rate_data",
        validators=[UserRoleValidator(Role.PATIENT)],
    )
    record_time = models.DateTimeField()
    # TODO ^ wish we could have the above fields in an interface class

    heart_rate = models.IntegerField()
