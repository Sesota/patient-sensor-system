import uuid

from ninja import Schema

from user.schema import UserOut


class ActivationIn(Schema):
    code: str
    name: str


class DeviceOut(Schema):
    user: UserOut
    name: str
    uuid: uuid.UUID
    is_active: bool
