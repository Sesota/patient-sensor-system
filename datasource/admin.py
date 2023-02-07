from django import forms
from django.contrib import admin

from .models import BloodPressureData, HeartRateData
from permissions.admin import AbilityAdminMixin


class BaseDatasourceAdmin(AbilityAdminMixin, admin.ModelAdmin):
    change_list_template = "datasource/change_list.html"
    list_filter = (("user", admin.RelatedOnlyFieldListFilter),)

    def get_form(self, request, obj=None, **kwargs):
        # Override the default form to disable the user field for
        # non-superusers
        form: forms.ModelForm = super().get_form(request, obj, **kwargs)

        if not form.base_fields or request.user.is_superuser:
            return form

        user_field: forms.ModelChoiceField = form.base_fields["user"]
        user_field.initial = request.user
        user_field.disabled = True

        return form


@admin.register(HeartRateData)
class HeartRateDataAdmin(BaseDatasourceAdmin):
    list_display = (
        "user",
        "record_time",
        "heart_rate",
    )


@admin.register(BloodPressureData)
class BloodPressureDataAdmin(BaseDatasourceAdmin):
    list_display = (
        "user",
        "record_time",
        "systolic_bp",
        "diastolic_bp",
    )
