import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.database import get_session
from mchome2.schemas.house import HouseCreate, HouseUpdate, HouseRead, HouseDetail
from mchome2.services import house_service

router = APIRouter(prefix="/api/houses", tags=["houses"])


@router.post("", response_model=HouseRead, status_code=201)
async def create_house(data: HouseCreate, session: AsyncSession = Depends(get_session)):
    house = await house_service.create_house(session, data)
    return house


@router.get("", response_model=list[HouseRead])
async def list_houses(session: AsyncSession = Depends(get_session)):
    return await house_service.list_houses(session)


@router.get("/{house_id}", response_model=HouseDetail)
async def get_house(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    detail = await house_service.get_house_detail(session, house_id)
    if not detail:
        raise HTTPException(status_code=404, detail="House not found")
    return detail


@router.put("/{house_id}", response_model=HouseRead)
async def update_house(house_id: uuid.UUID, data: HouseUpdate, session: AsyncSession = Depends(get_session)):
    house = await house_service.update_house(session, house_id, data)
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house


@router.delete("/{house_id}", status_code=204)
async def delete_house(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    deleted = await house_service.delete_house(session, house_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="House not found")
