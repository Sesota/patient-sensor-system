from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from ninja import Schema


@deconstructible
class SchemaValidator:
    def __init__(self, schema_cls: type[Schema]) -> None:
        self.schema_cls = schema_cls

    def __call__(self, value: Schema) -> None:
        try:
            if isinstance(value, dict):
                self.schema_cls.parse_obj(value)
            elif isinstance(value, list):
                [self.schema_cls.parse_obj(item) for item in value]
            else:
                raise ValidationError(
                    f"Value must be of type dict or list. Got {type(value)}"
                )
        except Exception as e:
            raise ValidationError(f"Invalid schema: {e}")

    def __eq__(self, other: "SchemaValidator") -> bool:
        return self.schema_cls.__name__ == other.schema_cls.__name__
