import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.database import get_session
from mchome2.schemas.room import RoomCreate, RoomUpdate, RoomRead, ScheduleCreate, ScheduleRead
from mchome2.schemas.reading import RoomCurrentResponse, PredictionRead
from mchome2.services import room_service, reading_service, prediction_service

router = APIRouter(prefix="/api/houses/{house_id}/rooms", tags=["rooms"])


@router.post("", response_model=RoomRead, status_code=201)
async def create_room(house_id: uuid.UUID, data: RoomCreate, session: AsyncSession = Depends(get_session)):
    room = await room_service.create_room(session, house_id, data)
    return room


@router.get("", response_model=list[RoomRead])
async def list_rooms(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await room_service.list_rooms(session, house_id)


@router.get("/{room_id}", response_model=RoomRead)
async def get_room(house_id: uuid.UUID, room_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    room = await room_service.get_room(session, house_id, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.put("/{room_id}", response_model=RoomRead)
async def update_room(house_id: uuid.UUID, room_id: uuid.UUID, data: RoomUpdate, session: AsyncSession = Depends(get_session)):
    room = await room_service.update_room(session, house_id, room_id, data)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.delete("/{room_id}", status_code=204)
async def delete_room(house_id: uuid.UUID, room_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    deleted = await room_service.delete_room(session, house_id, room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found")


# --- Schedules ---

@router.post("/{room_id}/schedules", response_model=ScheduleRead, status_code=201)
async def create_schedule(
    house_id: uuid.UUID, room_id: uuid.UUID, data: ScheduleCreate, session: AsyncSession = Depends(get_session)
):
    room = await room_service.get_room(session, house_id, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return await room_service.create_schedule(session, room_id, data)


@router.delete("/{room_id}/schedules/{schedule_id}", status_code=204)
async def delete_schedule(
    house_id: uuid.UUID, room_id: uuid.UUID, schedule_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    room = await room_service.get_room(session, house_id, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    deleted = await room_service.delete_schedule(session, schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")


@router.get("/{room_id}/schedules", response_model=list[ScheduleRead])
async def list_schedules(
    house_id: uuid.UUID, room_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    room = await room_service.get_room(session, house_id, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return await room_service.list_schedules(session, room_id)


# --- Live status ---

@router.get("/{room_id}/current", response_model=RoomCurrentResponse)
async def get_room_current(
    house_id: uuid.UUID, room_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    room = await room_service.get_room(session, house_id, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    temp = await reading_service.get_latest_room_temperature(session, room_id)
    windows_open, windows_total = await reading_service.get_room_window_status(session, room_id)
    return RoomCurrentResponse(
        room_id=room_id,
        temperature_c=temp,
        windows_open=windows_open,
        windows_total=windows_total,
    )


@router.get("/{room_id}/predictions", response_model=PredictionRead | None)
async def get_room_predictions(
    house_id: uuid.UUID, room_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    prediction = await prediction_service.get_latest_prediction(session, room_id)
    return prediction
