import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from mchome2.models.reading import BoilerAction


class TemperatureReadingRead(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    room_id: uuid.UUID
    temperature_c: float
    recorded_at: datetime

    model_config = {"from_attributes": True}


class WindowReadingRead(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    room_id: uuid.UUID
    is_open: bool
    recorded_at: datetime

    model_config = {"from_attributes": True}


class BoilerEventRead(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    house_id: uuid.UUID
    action: BoilerAction
    triggered_by: str
    recorded_at: datetime

    model_config = {"from_attributes": True}


class PredictionRead(BaseModel):
    id: uuid.UUID
    house_id: uuid.UUID
    room_id: uuid.UUID
    predicted_at: datetime
    schedule_json: list[dict[str, Any]]
    horizon_minutes: int

    model_config = {"from_attributes": True}


class BoilerStatusResponse(BaseModel):
    house_id: uuid.UUID
    is_on: bool
    last_event: BoilerEventRead | None = None


class BoilerOverrideRequest(BaseModel):
    action: BoilerAction


class RoomCurrentResponse(BaseModel):
    room_id: uuid.UUID
    temperature_c: float | None = None
    windows_open: int = 0
    windows_total: int = 0
