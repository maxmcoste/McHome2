import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from mchome2.config import settings
from mchome2.database import async_session_factory
from mchome2.models import House
from mchome2.services import reading_service, prediction_service

logger = logging.getLogger(__name__)


async def poll_sensors() -> None:
    """Poll all active sensors across all houses and store readings."""
    async with async_session_factory() as session:
        result = await session.execute(select(House))
        houses = result.scalars().all()
        for house in houses:
            try:
                await reading_service.poll_house_sensors(session, house.id)
                logger.debug("Polled sensors for house %s", house.name)
            except Exception:
                logger.exception("Error polling sensors for house %s", house.name)


async def run_predictions() -> None:
    """Run thermal predictions for all houses."""
    async with async_session_factory() as session:
        result = await session.execute(select(House))
        houses = result.scalars().all()
        for house in houses:
            try:
                predictions = await prediction_service.run_house_predictions(session, house.id)
                logger.debug("Generated %d predictions for house %s", len(predictions), house.name)
            except Exception:
                logger.exception("Error running predictions for house %s", house.name)


async def cleanup_old_readings() -> None:
    """Remove readings older than the retention period."""
    async with async_session_factory() as session:
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.reading_retention_days)
        try:
            count = await reading_service.cleanup_old_readings(session, cutoff)
            logger.info("Cleaned up %d old readings (before %s)", count, cutoff)
        except Exception:
            logger.exception("Error cleaning up old readings")
