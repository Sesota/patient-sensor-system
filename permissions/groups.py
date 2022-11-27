from django.contrib.auth.models import Group

from user.enums import Role


def define_role_groups() -> None:
    # patient
    patient_group, _ = Group.objects.get_or_create(name=Role.PATIENT.value)
    patient_group.permissions.set([])

    # supervisor
    supervisor_group, _ = Group.objects.get_or_create(
        name=Role.SUPERVISOR.value
    )
    supervisor_group.permissions.set([])
