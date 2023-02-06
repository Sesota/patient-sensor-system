from operator import attrgetter
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query import QuerySet
from django.http import JsonResponse

from datasource.enums import Datasources
from supervision.models import DatasourcesConfig
from user.models import User
from utils.charts import color_primary, color_danger
from utils.criteria import evaluate_criteria


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

    DS = Datasources(datasource)
    data: list[tuple[datetime, int]] = list(
        DS.db_model.objects.filter(user_id=user_id).values_list(
            "record_time", DS.variable_name
        )
    )
    chart_data = [
        {"x": int(record_time.timestamp()) * 1000, "y": value}
        for record_time, value in data
    ]
    user = User.objects.get(id=user_id)

    # TODO:
    ds_config: DatasourcesConfig | None
    alerting_indices: list[int]
    if request.user.is_supervisor:
        ds_config = DatasourcesConfig.objects.get(
            datasource=datasource,
            supervision__patient=user,
            supervision__supervisor=request.user,
        )
        alerting_indices = [
            i
            for i, data in enumerate(chart_data)
            if evaluate_criteria(ds_config.alerting_criteria, var=data["y"])
        ]
    elif request.user.is_patient:
        ds_config = None
        alerting_indices = []

    colors = [
        color_danger if i in alerting_indices else color_primary
        for i in range(len(chart_data))
    ]
    return JsonResponse(
        {
            "title": (
                f"{DS.db_model._meta.verbose_name_plural} for {user} Chart"
            ),
            "data": {
                "datasets": [
                    {
                        "label": (
                            f"{DS.db_model._meta.verbose_name}".title()
                        ),
                        "backgroundColor": colors,
                        "borderColor": colors,
                        "data": chart_data,
                    }
                ],
            },
        }
    )
