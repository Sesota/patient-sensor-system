from typing import Any

from ninja import Router
from datasource.schema import HeartRateUpload

from utils.auth import ApiKey, AuthenticatedHttpRequest

router = Router()


@router.post(
    "/upload/",
    auth=[ApiKey()],
    response={204: None, 403: dict[str, str]},
)
def upload_data(request: AuthenticatedHttpRequest, data: HeartRateUpload):
    if not request.ability.can("add", data.datasource.db_model):
        return 403, {
            "detail": (
                "You have not specified this datasource in your supervisions"
            )
        }
    data.create(user=request.auth, device=request.auth.last_used_device)
    return 204, None
