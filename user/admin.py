from typing import Any

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.http.request import HttpRequest

from .models import User
from device.admin import InlineDevice
from permissions.admin import AbilityAdminMixin


class CustomUserAdmin(AbilityAdminMixin, UserAdmin):
    inlines = [InlineDevice]
    list_display = ("username", "email", "first_name", "last_name", "role")
    list_filter = tuple()

    def get_form(self, request, obj=None, **kwargs):
        user: User = request.user
        form: type[forms.ModelForm[Any]] = super().get_form(request, obj, **kwargs)
        if not form.base_fields or user.is_superuser:
            return form

        role_field: forms.Field = form.base_fields["role"]
        role_field.disabled = True
        username_field: forms.Field = form.base_fields["username"]
        username_field.disabled = True

        return form

    def get_fieldsets(self, request: HttpRequest, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        return (
            (None, {"fields": ("username", "role")}),
            (
                _("Personal info"),
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "phone_number",
                    )
                },
            ),
        )


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
