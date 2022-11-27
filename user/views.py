from django.contrib.auth.views import LoginView

from user.forms import SignupForm


class SignupView(LoginView):
    form_class = SignupForm
    template_name = "user/signup.html"
