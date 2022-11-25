from django.contrib import admin

from .models import Supervision


@admin.register(Supervision)
class SupervisionAdmin(admin.ModelAdmin):
    list_display = ("supervisor", "patient", "datasources_configs")
