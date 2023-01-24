import re
from datetime import datetime
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from django.http.request import HttpRequest
from ninja.security import APIKeyHeader

from cancan.ability import Ability
from device.models import Device
from user.models import User


API_KEY_UUID_RE = (
    r"apikey"
    r" .+:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
API_KEY_CODE_RE = r"apikey [A-Z]{3}-[A-Z]{3}-[A-Z]{3}$"


class AuthenticatedHttpRequest(HttpRequest):
    ability: Ability
    auth: User


class ApiKey(APIKeyHeader):
    param_name = "Authorization"

    def authenticate(
        self, request: HttpRequest, key: Optional[str]
    ) -> Optional[AbstractBaseUser]:
        if key is None or re.match(API_KEY_UUID_RE, key) is None:
            return None

        username, uuid = key.split(" ")[1].split(":")

        if not username or not uuid:
            return None

        try:
            user: User = User.objects.get(username=username)
            device: Device = user.devices.get(uuid=uuid)
        except (User.DoesNotExist, Device.DoesNotExist):
            return None

        if not user.is_active or not device.is_active:
            return None

        device.last_used_at = datetime.now()
        device.save()

        return user


class DeviceActivationAuth(APIKeyHeader):
    param_name = "Authorization"

    def authenticate(
        self, request: HttpRequest, key: Optional[str]
    ) -> Optional[AbstractBaseUser]:
        if key is None or re.match(API_KEY_CODE_RE, key) is None:
            return None

        temp_code = key.split(" ")[1]

        device: Optional[Device] = Device.objects.filter(
            temp_code=temp_code
        ).last()

        if device is None or not device.user.is_active:
            return None

        device.last_used_at = datetime.now()
        device.save()

        return device.user
