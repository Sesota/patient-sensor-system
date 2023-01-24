from cancan.access_rules import AccessRules
from datasource.enums import Datasources
from device.models import Device
from supervision.models import Supervision, DatasourcesConfig
from user.models import User


def define_access_rules(user: User, rules: AccessRules) -> None:
    if not user.is_authenticated:
        return

    rules.allow("view", User, id=user.id)
    rules.allow("change", User, id=user.id)

    if user.is_patient:
        rules.allow("view", Device, user=user)
        rules.allow("add", Device)
        rules.allow("change", Device, user=user)
        rules.allow("delete", Device, user=user)

        rules.allow("view", Supervision, patient=user)
        rules.allow("add", Supervision)
        rules.allow("change", Supervision, patient=user)
        rules.allow("delete", Supervision, patient=user)

        rules.allow("view", DatasourcesConfig, supervision__patient=user)
        rules.allow("add", DatasourcesConfig)
        rules.allow("change", DatasourcesConfig, supervision__patient=user)
        rules.allow("delete", DatasourcesConfig, supervision__patient=user)

        for datasource in Datasources:
            rules.allow("view", datasource.db_model, user=user)

            # only allow adding to datasources that are specified in
            # supervisions
            if DatasourcesConfig.objects.filter(
                supervision__patient=user, datasource=datasource
            ).exists():
                rules.allow("add", datasource.db_model)

    if user.is_supervisor:
        rules.allow("view", Supervision, supervisor=user)
        rules.allow("change", Supervision, supervisor=user)
        rules.allow("delete", Supervision, supervisor=user)

        rules.allow("view", DatasourcesConfig, supervision__supervisor=user)
        rules.allow("change", DatasourcesConfig, supervision__supervisor=user)
        rules.allow("delete", DatasourcesConfig, supervision__supervisor=user)

        for datasource in Datasources:
            allowed_datasources_users = DatasourcesConfig.objects.filter(
                supervision__supervisor=user,
                datasource=datasource,
            ).values_list("supervision__patient_id", flat=True)
            rules.allow(
                "view",
                datasource.db_model,
                user_id__in=allowed_datasources_users,
            )
