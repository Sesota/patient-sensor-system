from django.contrib import admin

from .models import HeartRateData


@admin.register(HeartRateData)
class HeartRateDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'heart_rate', 'record_time')
