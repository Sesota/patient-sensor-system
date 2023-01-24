from typing import Any, Union

from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()


def normalize_subject(subject: Union[str, type[Any]]) -> type[Any]:
    """
    Accepts a class on which objects are to be checked for permissions.
    If the input is a str, it is assumed to be the path to a Django model and
    this function ties to imported it and return it.
    """
    if isinstance(subject, str):
        try:
            app_label, model_name = subject.split(".")
            return apps.get_model(app_label, model_name)
        except Exception:
            raise ValueError(f"Invalid model path: {subject}")
    return subject


class AccessRules:
    user: User
    rules: list[Any]
    action_aliases: dict[str, Any]

    def __init__(self, user: User):
        self.user = user
        self.rules = []
        self.action_aliases = {}

    def allow(self, action: str, subject, **kwargs) -> list[Any]:
        rule = {
            "type": "can",
            "action": action,
            "subject": normalize_subject(subject),
            "conditions": kwargs,
        }
        self.rules.append(rule)
        return rule

    def alias_action(self, action, alias):
        self.action_aliases[alias] = action

    def alias_to_action(self, alias):
        return self.action_aliases.get(alias, alias)
