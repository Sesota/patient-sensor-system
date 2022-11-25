from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import Role


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ADMIN,
    )
