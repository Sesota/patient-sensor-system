from ninja import Router
from device.models import Device
from device.schema import ActivationIn, DeviceOut

from utils.auth import AuthenticatedHttpRequest, DeviceActivationAuth

router = Router()


@router.post(
    "/activate/",
    auth=[DeviceActivationAuth()],
    response={200: DeviceOut, 400: dict[str, str]},
)
def activate_device(request: AuthenticatedHttpRequest, body: ActivationIn):
    device: Device = request.auth.last_used_device
    try:
        device.activate(body.code)
    except ValueError as e:
        return 400, {"details": str(e)}

    device.name = body.name
    device.save()

    return 200, DeviceOut.from_orm(device)
