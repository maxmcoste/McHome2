import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.models import Room, RoomSchedule
from mchome2.schemas.room import RoomCreate, RoomUpdate, ScheduleCreate


async def create_room(session: AsyncSession, house_id: uuid.UUID, data: RoomCreate) -> Room:
    room = Room(house_id=house_id, **data.model_dump())
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


async def list_rooms(session: AsyncSession, house_id: uuid.UUID) -> list[Room]:
    result = await session.execute(
        select(Room).where(Room.house_id == house_id).order_by(Room.name)
    )
    return list(result.scalars().all())


async def get_room(session: AsyncSession, house_id: uuid.UUID, room_id: uuid.UUID) -> Room | None:
    result = await session.execute(
        select(Room).where(and_(Room.id == room_id, Room.house_id == house_id))
    )
    return result.scalar_one_or_none()


async def update_room(session: AsyncSession, house_id: uuid.UUID, room_id: uuid.UUID, data: RoomUpdate) -> Room | None:
    room = await get_room(session, house_id, room_id)
    if not room:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(room, key, value)
    await session.commit()
    await session.refresh(room)
    return room


async def delete_room(session: AsyncSession, house_id: uuid.UUID, room_id: uuid.UUID) -> bool:
    room = await get_room(session, house_id, room_id)
    if not room:
        return False
    await session.delete(room)
    await session.commit()
    return True


async def create_schedule(session: AsyncSession, room_id: uuid.UUID, data: ScheduleCreate) -> RoomSchedule:
    schedule = RoomSchedule(room_id=room_id, **data.model_dump())
    session.add(schedule)
    await session.commit()
    await session.refresh(schedule)
    return schedule


async def list_schedules(session: AsyncSession, room_id: uuid.UUID) -> list[RoomSchedule]:
    result = await session.execute(
        select(RoomSchedule).where(RoomSchedule.room_id == room_id).order_by(RoomSchedule.time_start)
    )
    return list(result.scalars().all())


async def delete_schedule(session: AsyncSession, schedule_id: uuid.UUID) -> bool:
    result = await session.execute(
        select(RoomSchedule).where(RoomSchedule.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()
    if not schedule:
        return False
    await session.delete(schedule)
    await session.commit()
    return True


async def get_desired_temp(session: AsyncSession, room_id: uuid.UUID, day_of_week: int, current_time) -> float | None:
    result = await session.execute(
        select(RoomSchedule).where(
            and_(
                RoomSchedule.room_id == room_id,
                RoomSchedule.time_start <= current_time,
                RoomSchedule.time_end > current_time,
            )
        )
    )
    schedules = list(result.scalars().all())
    # Find best match: prefer specific-day schedule over every-day
    best = None
    for s in schedules:
        days = s.days_of_week
        is_every_day = not days  # None or empty list
        if is_every_day:
            if best is None:
                best = s
        elif day_of_week in days:
            best = s  # specific-day match always wins
    return best.desired_temp_c if best else None
