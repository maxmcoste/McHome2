import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.database import get_session
from mchome2.schemas.device import DeviceCreate, DeviceUpdate, DeviceRead
from mchome2.schemas.reading import BoilerStatusResponse, BoilerOverrideRequest, BoilerEventRead
from mchome2.models import DeviceType, BoilerAction
from mchome2.services import device_service, reading_service

router = APIRouter(tags=["devices"])


# --- Devices scoped under house ---

@router.post("/api/houses/{house_id}/devices", response_model=DeviceRead, status_code=201)
async def create_device(house_id: uuid.UUID, data: DeviceCreate, session: AsyncSession = Depends(get_session)):
    try:
        device = await device_service.create_device(session, house_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return device


@router.get("/api/houses/{house_id}/devices", response_model=list[DeviceRead])
async def list_devices(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await device_service.list_devices(session, house_id)


# --- Device-level operations ---

@router.get("/api/devices/{device_id}", response_model=DeviceRead)
async def get_device(device_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    device = await device_service.get_device(session, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/api/devices/{device_id}", response_model=DeviceRead)
async def update_device(device_id: uuid.UUID, data: DeviceUpdate, session: AsyncSession = Depends(get_session)):
    device = await device_service.update_device(session, device_id, data)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.delete("/api/devices/{device_id}", status_code=204)
async def delete_device(device_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    deleted = await device_service.delete_device(session, device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Device not found")


# --- Boiler status and override ---

@router.get("/api/houses/{house_id}/boiler/status", response_model=BoilerStatusResponse)
async def get_boiler_status(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    boiler_devices = await device_service.get_active_devices(session, house_id, DeviceType.boiler)
    is_on = False
    for dev in boiler_devices:
        driver = device_service.instantiate_driver(dev)
        is_on = await driver.is_on()
        break  # Use first active boiler

    last_event = await reading_service.get_latest_boiler_event(session, house_id)
    return BoilerStatusResponse(
        house_id=house_id,
        is_on=is_on,
        last_event=BoilerEventRead.model_validate(last_event) if last_event else None,
    )


@router.post("/api/houses/{house_id}/boiler/override", response_model=BoilerStatusResponse)
async def override_boiler(house_id: uuid.UUID, data: BoilerOverrideRequest, session: AsyncSession = Depends(get_session)):
    boiler_devices = await device_service.get_active_devices(session, house_id, DeviceType.boiler)
    if not boiler_devices:
        raise HTTPException(status_code=404, detail="No active boiler found for this house")

    for dev in boiler_devices:
        driver = device_service.instantiate_driver(dev)
        if data.action == BoilerAction.on:
            await driver.turn_on()
        else:
            await driver.turn_off()
        await reading_service.record_boiler_event(
            session, dev.id, house_id, data.action, "manual"
        )

    last_event = await reading_service.get_latest_boiler_event(session, house_id)
    return BoilerStatusResponse(
        house_id=house_id,
        is_on=data.action == BoilerAction.on,
        last_event=BoilerEventRead.model_validate(last_event) if last_event else None,
    )
