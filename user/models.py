from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from .enums import Role


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ADMIN,
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
