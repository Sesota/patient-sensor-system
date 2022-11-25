from django.db import models

from .schemas import SupervisionDatasourcesConfig
from user.validators import UserRoleValidator
from user.enums import Role
from utils.schemas import SchemaValidator


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
    datasources_configs = models.JSONField(
        default=list,
        validators=[SchemaValidator(SupervisionDatasourcesConfig)],
    )

    @property
    def datasources_configurations(self) -> list[SupervisionDatasourcesConfig]:
        return [
            SupervisionDatasourcesConfig.parse_obj(config)
            for config in self.datasources_configs
        ]

    @datasources_configurations.setter
    def datasources_configurations(
        self, value: list[SupervisionDatasourcesConfig]
    ) -> None:
        self.datasources_configs = [
            config.dict(exclude_unset=True) for config in value
        ]
