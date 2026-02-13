import uuid
from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.models import (
    TemperatureReading,
    WindowReading,
    BoilerEvent,
    BoilerAction,
    Device,
    DeviceType,
)
from mchome2.services import device_service


async def record_temperature(
    session: AsyncSession, device_id: uuid.UUID, room_id: uuid.UUID, temperature_c: float
) -> TemperatureReading:
    reading = TemperatureReading(device_id=device_id, room_id=room_id, temperature_c=temperature_c)
    session.add(reading)
    await session.commit()
    await session.refresh(reading)
    return reading


async def record_window(
    session: AsyncSession, device_id: uuid.UUID, room_id: uuid.UUID, is_open: bool
) -> WindowReading:
    reading = WindowReading(device_id=device_id, room_id=room_id, is_open=is_open)
    session.add(reading)
    await session.commit()
    await session.refresh(reading)
    return reading


async def record_boiler_event(
    session: AsyncSession, device_id: uuid.UUID, house_id: uuid.UUID, action: BoilerAction, triggered_by: str = "prediction"
) -> BoilerEvent:
    event = BoilerEvent(device_id=device_id, house_id=house_id, action=action, triggered_by=triggered_by)
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def get_temperature_readings(
    session: AsyncSession,
    house_id: uuid.UUID | None = None,
    room_id: uuid.UUID | None = None,
    from_dt: datetime | None = None,
    to_dt: datetime | None = None,
    limit: int = 100,
) -> list[TemperatureReading]:
    stmt = select(TemperatureReading)
    conditions = []
    if room_id:
        conditions.append(TemperatureReading.room_id == room_id)
    if house_id and not room_id:
        # Join through device to filter by house
        stmt = stmt.join(Device)
        conditions.append(Device.house_id == house_id)
    if from_dt:
        conditions.append(TemperatureReading.recorded_at >= from_dt)
    if to_dt:
        conditions.append(TemperatureReading.recorded_at <= to_dt)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(TemperatureReading.recorded_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_window_readings(
    session: AsyncSession,
    house_id: uuid.UUID | None = None,
    room_id: uuid.UUID | None = None,
    from_dt: datetime | None = None,
    to_dt: datetime | None = None,
    limit: int = 100,
) -> list[WindowReading]:
    stmt = select(WindowReading)
    conditions = []
    if room_id:
        conditions.append(WindowReading.room_id == room_id)
    if house_id and not room_id:
        stmt = stmt.join(Device)
        conditions.append(Device.house_id == house_id)
    if from_dt:
        conditions.append(WindowReading.recorded_at >= from_dt)
    if to_dt:
        conditions.append(WindowReading.recorded_at <= to_dt)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(WindowReading.recorded_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_latest_boiler_event(session: AsyncSession, house_id: uuid.UUID) -> BoilerEvent | None:
    result = await session.execute(
        select(BoilerEvent)
        .where(BoilerEvent.house_id == house_id)
        .order_by(BoilerEvent.recorded_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_latest_room_temperature(session: AsyncSession, room_id: uuid.UUID) -> float | None:
    result = await session.execute(
        select(TemperatureReading)
        .where(TemperatureReading.room_id == room_id)
        .order_by(TemperatureReading.recorded_at.desc())
        .limit(1)
    )
    reading = result.scalar_one_or_none()
    return reading.temperature_c if reading else None


async def get_room_window_status(session: AsyncSession, room_id: uuid.UUID) -> tuple[int, int]:
    """Returns (windows_open, windows_total) based on latest reading per device."""
    devices = await device_service.get_active_devices(
        session, house_id=None, device_type=DeviceType.window_sensor, room_id=room_id
    )
    # Fallback: query directly for window sensors in this room
    if not devices:
        device_result = await session.execute(
            select(Device).where(
                and_(Device.room_id == room_id, Device.device_type == DeviceType.window_sensor, Device.is_active.is_(True))
            )
        )
        devices = list(device_result.scalars().all())

    windows_open = 0
    windows_total = len(devices)
    for dev in devices:
        result = await session.execute(
            select(WindowReading)
            .where(WindowReading.device_id == dev.id)
            .order_by(WindowReading.recorded_at.desc())
            .limit(1)
        )
        reading = result.scalar_one_or_none()
        if reading and reading.is_open:
            windows_open += 1
    return windows_open, windows_total


async def poll_house_sensors(session: AsyncSession, house_id: uuid.UUID) -> None:
    """Poll all active sensors for a house and record readings."""
    # Temperature sensors
    temp_devices = await device_service.get_active_devices(session, house_id, DeviceType.temperature_sensor)
    for dev in temp_devices:
        if not dev.room_id:
            continue
        driver = device_service.instantiate_driver(dev)
        temp = await driver.read_temperature()
        await record_temperature(session, dev.id, dev.room_id, temp)

    # Window sensors
    window_devices = await device_service.get_active_devices(session, house_id, DeviceType.window_sensor)
    for dev in window_devices:
        if not dev.room_id:
            continue
        driver = device_service.instantiate_driver(dev)
        is_open = await driver.read_is_open()
        await record_window(session, dev.id, dev.room_id, is_open)


async def cleanup_old_readings(session: AsyncSession, before: datetime) -> int:
    """Delete readings older than the given datetime. Returns count deleted."""
    from sqlalchemy import delete

    count = 0
    for model in [TemperatureReading, WindowReading, BoilerEvent]:
        result = await session.execute(
            delete(model).where(model.recorded_at < before)
        )
        count += result.rowcount
    await session.commit()
    return count
