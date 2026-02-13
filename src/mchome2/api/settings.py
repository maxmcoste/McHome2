from fastapi import APIRouter

from mchome2.config import settings, save_settings
from mchome2.schemas.settings import SettingsRead, SettingsUpdate

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsRead)
async def get_settings():
    return SettingsRead(
        database_url=settings.database_url,
        sensor_poll_interval_seconds=settings.sensor_poll_interval_seconds,
        prediction_interval_seconds=settings.prediction_interval_seconds,
        prediction_horizon_minutes=settings.prediction_horizon_minutes,
        reading_retention_days=settings.reading_retention_days,
        default_boiler_power_watts=settings.default_boiler_power_watts,
    )


@router.put("", response_model=SettingsRead)
async def update_settings(data: SettingsUpdate):
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(settings, key, value)
    save_settings(updates)
    return SettingsRead(
        database_url=settings.database_url,
        sensor_poll_interval_seconds=settings.sensor_poll_interval_seconds,
        prediction_interval_seconds=settings.prediction_interval_seconds,
        prediction_horizon_minutes=settings.prediction_horizon_minutes,
        reading_retention_days=settings.reading_retention_days,
        default_boiler_power_watts=settings.default_boiler_power_watts,
    )
