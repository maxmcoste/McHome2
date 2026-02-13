import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.database import get_session
from mchome2.schemas.reading import TemperatureReadingRead, WindowReadingRead
from mchome2.services import reading_service

router = APIRouter(prefix="/api/readings", tags=["readings"])


@router.get("/temperature", response_model=list[TemperatureReadingRead])
async def get_temperature_readings(
    house_id: uuid.UUID | None = Query(None),
    room_id: uuid.UUID | None = Query(None),
    from_dt: datetime | None = Query(None, alias="from"),
    to_dt: datetime | None = Query(None, alias="to"),
    limit: int = Query(100, le=1000),
    session: AsyncSession = Depends(get_session),
):
    return await reading_service.get_temperature_readings(session, house_id, room_id, from_dt, to_dt, limit)


@router.get("/windows", response_model=list[WindowReadingRead])
async def get_window_readings(
    house_id: uuid.UUID | None = Query(None),
    room_id: uuid.UUID | None = Query(None),
    from_dt: datetime | None = Query(None, alias="from"),
    to_dt: datetime | None = Query(None, alias="to"),
    limit: int = Query(100, le=1000),
    session: AsyncSession = Depends(get_session),
):
    return await reading_service.get_window_readings(session, house_id, room_id, from_dt, to_dt, limit)
