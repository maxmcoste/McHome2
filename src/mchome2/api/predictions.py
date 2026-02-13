import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.database import get_session
from mchome2.schemas.reading import PredictionRead
from mchome2.services import prediction_service

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.post("/run/{house_id}", response_model=list[PredictionRead])
async def trigger_predictions(house_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    predictions = await prediction_service.run_house_predictions(session, house_id)
    if not predictions:
        raise HTTPException(status_code=404, detail="House not found or no rooms")
    return predictions
