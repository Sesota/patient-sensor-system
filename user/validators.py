from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .enums import Role

if TYPE_CHECKING:
    from .models import User


@deconstructible
class UserRoleValidator:
    def __init__(self, role: Role) -> None:
        self.role = role

    def __call__(self, value: "User") -> None:
        if value.role != self.role:
            raise ValidationError(
                f"User must have role {self.role}. Got {value.role}"
            )

    def __eq__(self, other: "UserRoleValidator") -> bool:
        return self.role == other.role
