from django.contrib import admin

from .models import Supervision
from permissions.admin import AbilityModelAdminMixin


@admin.register(Supervision)
class SupervisionAdmin(AbilityModelAdminMixin, admin.ModelAdmin):
    list_display = ("supervisor", "patient", "datasources_configs")
