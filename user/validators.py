from typing import Union

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .enums import Role
from .models import User


@deconstructible
class UserRoleValidator:
    def __init__(self, role: Role) -> None:
        self.role = role

    def __call__(self, value: Union[int, "User"]) -> None:
        if isinstance(value, int):
            user = User.objects.get(pk=value)
        else:
            user = value
        if user.role != self.role:
            raise ValidationError(
                f"User must have role {self.role}. Got {user.role}"
            )

    def __eq__(self, other: "UserRoleValidator") -> bool:
        return self.role == other.role
