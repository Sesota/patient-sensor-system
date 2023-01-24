from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from config.routers import api_v1
from user import views as user_views

urlpatterns = [
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
    path("admin/", admin.site.urls),
    path("api/", api_v1.urls),
    path('datasource/', include('datasource.urls')),
]
