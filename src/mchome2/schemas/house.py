import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class HouseCreate(BaseModel):
    name: str = Field(..., max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str = Field(default="UTC", max_length=50)


class HouseUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    timezone: str | None = Field(None, max_length=50)


class HouseRead(BaseModel):
    id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    timezone: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HouseDetail(HouseRead):
    room_count: int = 0
    device_count: int = 0
