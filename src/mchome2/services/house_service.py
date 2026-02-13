import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.models import House, Room, Device
from mchome2.schemas.house import HouseCreate, HouseUpdate, HouseDetail


async def create_house(session: AsyncSession, data: HouseCreate) -> House:
    house = House(**data.model_dump())
    session.add(house)
    await session.commit()
    await session.refresh(house)
    return house


async def list_houses(session: AsyncSession) -> list[House]:
    result = await session.execute(select(House).order_by(House.name))
    return list(result.scalars().all())


async def get_house(session: AsyncSession, house_id: uuid.UUID) -> House | None:
    return await session.get(House, house_id)


async def get_house_detail(session: AsyncSession, house_id: uuid.UUID) -> HouseDetail | None:
    house = await session.get(House, house_id)
    if not house:
        return None

    room_count_result = await session.execute(
        select(func.count()).select_from(Room).where(Room.house_id == house_id)
    )
    device_count_result = await session.execute(
        select(func.count()).select_from(Device).where(Device.house_id == house_id)
    )

    return HouseDetail(
        **{c.key: getattr(house, c.key) for c in House.__table__.columns},
        room_count=room_count_result.scalar_one(),
        device_count=device_count_result.scalar_one(),
    )


async def update_house(session: AsyncSession, house_id: uuid.UUID, data: HouseUpdate) -> House | None:
    house = await session.get(House, house_id)
    if not house:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(house, key, value)
    await session.commit()
    await session.refresh(house)
    return house


async def delete_house(session: AsyncSession, house_id: uuid.UUID) -> bool:
    house = await session.get(House, house_id)
    if not house:
        return False
    await session.delete(house)
    await session.commit()
    return True
