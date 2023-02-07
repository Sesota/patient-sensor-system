from typing import Any


class ClassEnumMixin:
    @property
    def klass(self) -> type[Any]:
        raise NotImplementedError

    def __getattr__(self, name: str) -> str:
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(
                object.__getattribute__(self, "klass"), name
            )
