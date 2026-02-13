import uuid
from datetime import datetime

from pydantic import BaseModel


class RoomDashboard(BaseModel):
    room_id: uuid.UUID
    room_name: str
    temperature_c: float | None = None
    desired_temp_c: float | None = None
    windows_open: int = 0
    windows_total: int = 0
    has_prediction: bool = False


class HouseDashboard(BaseModel):
    house_id: uuid.UUID
    house_name: str
    boiler_is_on: bool = False
    last_boiler_event_at: datetime | None = None
    rooms: list[RoomDashboard] = []


class DashboardResponse(BaseModel):
    houses: list[HouseDashboard] = []
