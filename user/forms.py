from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError as ORMValidationError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .enums import Role
from .models import User

allowed_roles = Role.choices[1:]

class SignupForm(AuthenticationForm):
    role = forms.ChoiceField(choices=allowed_roles)

    error_messages = {
        "invalid_params": _("The field %(field)s is not valid: "),
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        role = self.cleaned_data.get("role")

        if not username or not password or not role:
            return self.cleaned_data

        try:
            User(username=username, password=password, role=role).full_clean()
            self.user_cache: User = User.objects.create_user(
                username=username,
                password=password,
                role=role,
                is_staff=True,
            )
        except ORMValidationError as e:
            raise self.get_invalid_params_error(e)

        self.user_cache.set_groups()

        return super().clean()

    def get_invalid_params_error(
        self, e: ORMValidationError
    ) -> ValidationError:
        field_name = list(e.error_dict)[0]
        field_error: ORMValidationError = e.error_dict[field_name][0]
        error = ValidationError(
            self.error_messages["invalid_params"] + field_error.message,
            code="invalid_params",
            params={
                "field": field_name,
                **field_error.params,
            },
        )
        return error
