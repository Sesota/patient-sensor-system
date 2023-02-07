from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from config.routers import api_v1
from user import views as user_views

urlpatterns = [
    # admin paths
    path(
        "admin/signup/",
        user_views.SignupView.as_view(),
        name="signup",
    ),
    path(
        "admin/login/",
        auth_views.LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("admin/", admin.site.urls),
    # app paths
    path("api/", api_v1.urls),
    path("datasource/", include("datasource.urls")),
]
