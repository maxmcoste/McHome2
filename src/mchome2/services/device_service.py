import uuid
from typing import Any

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.models import Device, DeviceType
from mchome2.schemas.device import DeviceCreate, DeviceUpdate
from mchome2.hardware.registry import registry


async def create_device(session: AsyncSession, house_id: uuid.UUID, data: DeviceCreate) -> Device:
    # Validate driver exists
    registry.create_device(data.device_type.value, data.driver_name, data.config_json)

    device = Device(house_id=house_id, **data.model_dump())
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


async def list_devices(session: AsyncSession, house_id: uuid.UUID) -> list[Device]:
    result = await session.execute(
        select(Device).where(Device.house_id == house_id).order_by(Device.name)
    )
    return list(result.scalars().all())


async def get_device(session: AsyncSession, device_id: uuid.UUID) -> Device | None:
    return await session.get(Device, device_id)


async def update_device(session: AsyncSession, device_id: uuid.UUID, data: DeviceUpdate) -> Device | None:
    device = await session.get(Device, device_id)
    if not device:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(device, key, value)
    await session.commit()
    await session.refresh(device)
    return device


async def delete_device(session: AsyncSession, device_id: uuid.UUID) -> bool:
    device = await session.get(Device, device_id)
    if not device:
        return False
    await session.delete(device)
    await session.commit()
    return True


async def get_active_devices(
    session: AsyncSession, house_id: uuid.UUID, device_type: DeviceType, room_id: uuid.UUID | None = None
) -> list[Device]:
    conditions = [Device.house_id == house_id, Device.device_type == device_type, Device.is_active.is_(True)]
    if room_id is not None:
        conditions.append(Device.room_id == room_id)
    result = await session.execute(select(Device).where(and_(*conditions)))
    return list(result.scalars().all())


def instantiate_driver(device: Device) -> Any:
    from mchome2.config import settings

    config = device.config_json or {}
    config.setdefault("device_id", str(device.id))
    if device.driver_name == "tado" and settings.tado_refresh_token:
        config.setdefault("refresh_token", settings.tado_refresh_token)
    return registry.create_device(device.device_type.value, device.driver_name, config)
