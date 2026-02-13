import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from mchome2.models.device import DeviceType


class DeviceCreate(BaseModel):
    room_id: uuid.UUID | None = None
    device_type: DeviceType
    driver_name: str = Field(default="simulator", max_length=100)
    config_json: dict[str, Any] | None = None
    name: str = Field(..., max_length=255)


class DeviceUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    is_active: bool | None = None
    config_json: dict[str, Any] | None = None


class DeviceRead(BaseModel):
    id: uuid.UUID
    house_id: uuid.UUID
    room_id: uuid.UUID | None
    device_type: DeviceType
    driver_name: str
    config_json: dict[str, Any] | None
    name: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
