from typing import Any

from django import forms
from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms import BaseInlineFormSet

from .forms import SupervisionAdminForm
from .models import DatasourcesConfig, Supervision
from permissions.admin import AbilityAdminMixin
from user.enums import Role
from user.models import User


class DatasourcesConfigInline(AbilityAdminMixin, admin.TabularInline):
    model = DatasourcesConfig
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset: type[BaseInlineFormSet] = super().get_formset(
            request, obj, **kwargs
        )
        if request.user.is_superuser:
            return formset

        if request.user.is_supervisor:
            formset.form.base_fields["datasource"].disabled = True
        elif request.user.is_patient:
            formset.form.base_fields["alerting_medium"].disabled = True
            formset.form.base_fields["alerting_criteria"].disabled = True
        return formset


@admin.register(Supervision)
class SupervisionAdmin(AbilityAdminMixin, admin.ModelAdmin):
    form = SupervisionAdminForm
    inlines = [DatasourcesConfigInline]
    list_display = (
        "__str__",
        "supervisor",
        "patient",
    )

    def get_form(self, request, obj=None, **kwargs):
        form: type[forms.ModelForm[Any]] = super().get_form(
            request, obj, **kwargs
        )

        if not form.base_fields or request.user.is_superuser:
            return form

        supervisor_field: forms.ModelChoiceField = form.base_fields[
            "supervisor"
        ]
        patient_field: forms.ModelChoiceField = form.base_fields["patient"]

        patient_field.initial = request.user
        patient_field.disabled = True

        if request.user.is_patient:
            qs: "QuerySet[User]" = User.objects.filter(role=Role.SUPERVISOR)
            if obj is None:  # add form
                qs = qs.exclude(
                    id__in=request.user.supervisors.values_list(
                        "supervisor_id", flat=True
                    )
                )
            else:  # change form
                supervisor_field.disabled = True

            supervisor_field.queryset = qs

        if request.user.is_supervisor:
            supervisor_field.disabled = True

        return form
