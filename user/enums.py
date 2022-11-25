from django.db import models


class Role(models.TextChoices):
    ADMIN = "admin"
    PATIENT = "patient"
    SUPERVISOR = "supervisor"
