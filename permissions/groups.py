from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from user.enums import Role


def get_model_permissions(model):
    content_type = ContentType.objects.get_for_model(model)
    return list(Permission.objects.filter(content_type=content_type))


def define_role_groups() -> None:
    # patient
    patient_group, _ = Group.objects.get_or_create(name=Role.PATIENT.value)
    patient_group.permissions.set([])
    # patient_group.permissions.add(*get_model_permissions(Supervision))

    # supervisor
    supervisor_group, _ = Group.objects.get_or_create(
        name=Role.SUPERVISOR.value
    )
    supervisor_group.permissions.set([])
