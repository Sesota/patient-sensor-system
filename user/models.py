from typing import TYPE_CHECKING, Optional
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator
from django.db import models

from .enums import Role

if TYPE_CHECKING:
    from device.models import Device


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ADMIN,
    )
    phone_number = models.CharField(
        max_length=31,
        blank=True,
        validators=[RegexValidator(regex=r"^\+?[0-9]{10,15}$")],
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.username
        )

    def set_groups(self):
        # NOTE must be called after every user creation
        self.groups.clear()
        group = Group.objects.get(name=self.role)
        self.groups.add(group)

    @property
    def is_patient(self):
        return self.role == Role.PATIENT

    @property
    def is_supervisor(self):
        return self.role == Role.SUPERVISOR

    @property
    def last_used_device(self) -> Optional["Device"]:
        return self.devices.order_by("last_used_at").last()
