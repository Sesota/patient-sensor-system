from django.contrib import admin

from .models import HeartRateData
from permissions.admin import AbilityModelAdminMixin


@admin.register(HeartRateData)
class HeartRateDataAdmin(AbilityModelAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'heart_rate', 'record_time')
