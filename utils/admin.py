from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class CustomAdminSite(admin.AdminSite):
    site_header = "Patient Health Monitoring System"
    site_title = "Patient Health Monitoring System"
    index_title = "Dashboard"
    site_url = None


class CustomAdminConfig(AdminConfig):
    default_site = "utils.admin.CustomAdminSite"
