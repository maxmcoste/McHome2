import uuid
from datetime import datetime, time

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    name: str = Field(..., max_length=255)
    volume_m3: float = Field(default=50.0, gt=0)
    insulation_factor: float = Field(default=0.5, ge=0, le=1)
    orientation: str = Field(default="S", pattern=r"^(N|S|E|W|NE|NW|SE|SW)$")
    window_area_m2: float = Field(default=2.0, ge=0)


class RoomUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    volume_m3: float | None = Field(None, gt=0)
    insulation_factor: float | None = Field(None, ge=0, le=1)
    orientation: str | None = Field(None, pattern=r"^(N|S|E|W|NE|NW|SE|SW)$")
    window_area_m2: float | None = Field(None, ge=0)


class RoomRead(BaseModel):
    id: uuid.UUID
    house_id: uuid.UUID
    name: str
    volume_m3: float
    insulation_factor: float
    orientation: str
    window_area_m2: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ScheduleCreate(BaseModel):
    days_of_week: list[int] | None = Field(None, description="List of day numbers 0-6 (Mon-Sun). None or empty = every day.")
    time_start: time
    time_end: time
    desired_temp_c: float = Field(..., ge=5, le=35)


class ScheduleRead(BaseModel):
    id: uuid.UUID
    room_id: uuid.UUID
    days_of_week: list[int] | None
    time_start: time
    time_end: time
    desired_temp_c: float

    model_config = {"from_attributes": True}
