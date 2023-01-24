from django import forms
from django.contrib import admin

from .models import HeartRateData
from permissions.admin import AbilityAdminMixin


@admin.register(HeartRateData)
class HeartRateDataAdmin(AbilityAdminMixin, admin.ModelAdmin):
    change_list_template = "datasource/change_list.html"
    list_display = ("user", "heart_rate", "record_time")
    list_filter = (("user", admin.RelatedOnlyFieldListFilter),)

    def get_form(self, request, obj=None, **kwargs):
        form: forms.ModelForm = super().get_form(request, obj, **kwargs)

        if not form.base_fields or request.user.is_superuser:
            return form

        user_field: forms.ModelChoiceField = form.base_fields["user"]
        user_field.initial = request.user
        user_field.disabled = True

        return form
