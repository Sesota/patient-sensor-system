from datetime import timedelta, datetime
import random
import string
import uuid

from django.db import models

from user.enums import Role
from user.validators import UserRoleValidator


class Device(models.Model):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="devices",
        validators=[UserRoleValidator(Role.PATIENT)],
    )
    uuid = models.UUIDField(max_length=255, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    temp_code = models.CharField(max_length=255, blank=True, null=True)
    temp_code_expires_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    def request_activation(self) -> str:
        self.is_active = False
        self.temp_code = self._generate_temp_code()
        self.temp_code_expires_at = datetime.now() + timedelta(minutes=5)
        self.save()
        return self.temp_code

    def activate(self, temp_code: str) -> None:
        if not self.temp_code or not self.temp_code_expires_at:
            raise ValueError("Device is not awaiting activation")
        if self.temp_code != temp_code:
            raise ValueError("Invalid activation code")
        if self.temp_code_expires_at < datetime.now().replace(
            tzinfo=self.temp_code_expires_at.tzinfo
        ):
            raise ValueError("Activation code has expired")
        self.is_active = True
        self.temp_code = None
        self.temp_code_expires_at = None
        self.uuid = uuid.uuid4()
        self.save()

    def _generate_temp_code(self) -> str:
        return "-".join(
            "".join([random.choice(string.ascii_uppercase) for _ in range(3)])
            for _ in range(3)
        )

    def __str__(self) -> str:
        return self.name
