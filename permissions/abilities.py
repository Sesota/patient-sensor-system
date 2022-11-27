from cancan.access_rules import AccessRules
from supervision.models import Supervision
from user.models import User


def define_access_rules(user: User, rules: AccessRules) -> None:
    if not user.is_authenticated:
        return

    if user.is_patient:
        rules.allow("view", Supervision, patient=user)
        rules.allow("add", Supervision)
    if user.is_supervisor:
        rules.allow("view", Supervision, supervisor=user)
