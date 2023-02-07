from operator import attrgetter
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query import QuerySet
from django.http import JsonResponse

from datasource.enums import Datasources
from datasource.models import BaseDatasource
from supervision.models import DatasourcesConfig, Supervision
from user.models import User
from utils.charts import color_palette, color_danger


def accesses_chart(user: User, datasource: str) -> list[User]:
    users: "QuerySet[User]"
    if (
        user.is_patient
        and DatasourcesConfig.objects.filter(
            datasource=datasource, supervision__patient=user
        ).exists()
    ):
        users = User.objects.filter(id=user.id)
    elif user.is_supervisor:
        users = User.objects.filter(
            id__in=DatasourcesConfig.objects.filter(
                supervision__supervisor=user, datasource=datasource
            ).values_list("supervision__patient_id", flat=True)
        )
    return list(users)


@staff_member_required
def get_filter_options(request, datasource: str):
    data = {
        "options": [
            {
                "label": str(user),
                "id": user.id,
            }
            for user in accesses_chart(request.user, datasource)
        ]
    }
    return JsonResponse(data)


@staff_member_required
def get_chart_data(request, datasource: str, user_id: int):
    if user_id not in map(
        attrgetter("id"), accesses_chart(request.user, datasource)
    ):
        return JsonResponse({"details": "Access denied"}, status=403)

    user = User.objects.get(id=user_id)
    DS = Datasources(datasource)

    datasource_records: "QuerySet[BaseDatasource]" = (
        DS.db_model.objects.filter(user_id=user_id)
    ).order_by("record_time", "id")

    record_times: list[datetime] = list(
        datasource_records.values_list("record_time", flat=True)
    )
    sensor_data: list[tuple[int, ...]] = list(
        datasource_records.values_list(*DS.variable_names)
    )

    alerting_indices: list[int]
    if request.user.is_supervisor:
        supervision: "QuerySet[Supervision]" = Supervision.objects.filter(
            supervisor=request.user, patient=user
        )
        alerting_indices = [
            i
            for i, record in enumerate(datasource_records)
            if record.get_alerting_supervisions(supervision)
        ]
    elif request.user.is_patient:
        alerting_indices = []

    colors = [
        color_danger if i in alerting_indices else ""
        for i in range(len(record_times))
    ]

    datasets = []
    for i, variable_name in enumerate(DS.variable_names):
        specific_colors = list(
            map(lambda c: c if c else color_palette[i], colors)
        )
        datasets.append(
            {
                "label": variable_name.replace("_", " ").title(),
                "data": [
                    {"x": int(record_time.timestamp()) * 1000, "y": values[i]}
                    for record_time, values in zip(record_times, sensor_data)
                ],
                "borderColor": [color_palette[i]] * len(record_times),
                "backgroundColor": specific_colors,
            }
        )
    return JsonResponse(
        {
            "title": (
                f"{DS.db_model._meta.verbose_name_plural} for {user} Chart"
            ),
            "data": {
                "datasets": datasets,
            },
        }
    )
