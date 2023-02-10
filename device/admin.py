from django import forms
from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Device
from permissions.admin import AbilityAdminMixin


@admin.register(Device)
class DeviceAdmin(AbilityAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "temp_code",
        "temp_code_expires_at",
        "request_activation",
    )
    list_filter = ("is_active",)
    search_fields = ("user__username", "name")
    fields = ("uuid", "name", "is_active")
    readonly_fields = ("uuid", "name", "is_active")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "request-activation/<int:pk>/",
                self.admin_site.admin_view(self.request_activation_view),
                name="request-activation",
            )
        ]
        return custom_urls + urls

    @admin.display
    def request_activation(self, obj):
        return format_html(
            '<a href="{}" class="button">Request activation</a>',
            reverse("admin:request-activation", args=[obj.pk]),
        )

    def request_activation_view(self, request, pk):
        device: Device = Device.objects.get(id=pk)
        tempcode = device.request_activation()
        self.message_user(
            request,
            "Request Succeeded. Please enter the device record's temporary"
            f" code ({tempcode}) in the device to complete the activation.",
        )
        return HttpResponseRedirect(reverse("admin:device_device_changelist"))

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class InlineDeviceForm(forms.ModelForm):
    def has_changed(self):
        return True


class InlineDevice(AbilityAdminMixin, admin.StackedInline):
    form = InlineDeviceForm
    model = Device
    extra = 0
    fields = ("uuid", "name", "is_active")

    def get_formset(self, request, obj=None, **kwargs):
        formset: type[forms.BaseInlineFormSet] = super().get_formset(
            request, obj, **kwargs
        )
        if request.user.is_superuser:
            return formset

        formset.form.base_fields["uuid"].disabled = True
        formset.form.base_fields["name"].disabled = True
        formset.form.base_fields["is_active"].disabled = True

        return formset
