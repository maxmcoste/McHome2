import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.database import get_session
from mchome2.schemas.dashboard import DashboardResponse, HouseDashboard, RoomDashboard
from mchome2.services import house_service, room_service, reading_service, prediction_service, device_service
from mchome2.models import DeviceType

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
async def get_dashboard(session: AsyncSession = Depends(get_session)):
    houses = await house_service.list_houses(session)
    result = []
    for house in houses:
        house_dash = await _build_house_dashboard(session, house)
        result.append(house_dash)
    return DashboardResponse(houses=result)


@router.get("/{house_id}", response_model=HouseDashboard)
async def get_house_dashboard(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    house = await house_service.get_house(session, house_id)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return await _build_house_dashboard(session, house)


async def _build_house_dashboard(session: AsyncSession, house) -> HouseDashboard:
    now = datetime.now(timezone.utc)

    # Boiler status
    boiler_is_on = False
    last_boiler_at = None
    boiler_devices = await device_service.get_active_devices(session, house.id, DeviceType.boiler)
    for dev in boiler_devices:
        driver = device_service.instantiate_driver(dev)
        boiler_is_on = await driver.is_on()
        break
    last_event = await reading_service.get_latest_boiler_event(session, house.id)
    if last_event:
        last_boiler_at = last_event.recorded_at

    # Rooms
    rooms = await room_service.list_rooms(session, house.id)
    room_dashboards = []
    for room in rooms:
        temp = await reading_service.get_latest_room_temperature(session, room.id)
        windows_open, windows_total = await reading_service.get_room_window_status(session, room.id)
        desired = await room_service.get_desired_temp(session, room.id, now.weekday(), now.time())
        prediction = await prediction_service.get_latest_prediction(session, room.id)
        room_dashboards.append(RoomDashboard(
            room_id=room.id,
            room_name=room.name,
            temperature_c=temp,
            desired_temp_c=desired,
            windows_open=windows_open,
            windows_total=windows_total,
            has_prediction=prediction is not None,
        ))

    return HouseDashboard(
        house_id=house.id,
        house_name=house.name,
        boiler_is_on=boiler_is_on,
        last_boiler_event_at=last_boiler_at,
        rooms=room_dashboards,
    )
