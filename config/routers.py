import json

from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from pydantic.json import pydantic_encoder

from datasource.api import router as datasource_router
from device.api import router as device_router

api_v1 = NinjaAPI(version="1.0.0")

api_v1.add_router(
    "/device/",
    device_router,
    tags=["device"],
)
api_v1.add_router(
    "/datasource/",
    datasource_router,
    tags=["datasource"],
)

# -----------------------------------------------------------------------------
# API handlers


@api_v1.exception_handler(PydanticValidationError)
def pydantic_validation_errors(
    request: HttpRequest, exc: PydanticValidationError
) -> HttpResponse:
    return api_v1.create_response(
        request, {"details": json.loads(exc.json())}, status=400
    )


# -----------------------------------------------------------------------------


@api_v1.exception_handler(NinjaValidationError)
def ninja_validation_errors(
    request: HttpRequest, exc: NinjaValidationError
) -> HttpResponse:
    return api_v1.create_response(
        request,
        {
            "detail": json.loads(
                json.dumps(exc.errors, default=pydantic_encoder)
            )
        },
        status=400,
    )


# -----------------------------------------------------------------------------
