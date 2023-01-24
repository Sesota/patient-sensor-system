from django.db import models


class AlertingMedium(models.TextChoices):
    OFF = "off"
    SMS = "sms"
    EMAIL = "email"
