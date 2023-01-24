from django.urls import path

from .views import get_chart_data, get_filter_options

urlpatterns = [
    path(
        "chart/filter-options/<str:datasource>/",
        get_filter_options,
        name="chart-filter-options",
    ),
    path(
        "chart/data/<str:datasource>/<int:user_id>/",
        get_chart_data,
        name="chart-data",
    ),
]
