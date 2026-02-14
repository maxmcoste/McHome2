import json
import os
from pathlib import Path

from pydantic_settings import BaseSettings

SETTINGS_FILE = os.environ.get("MCHOME2_SETTINGS_FILE", None)


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://localhost:5432/mchome2"
    sensor_poll_interval_seconds: int = 30
    prediction_interval_seconds: int = 300
    prediction_horizon_minutes: int = 240
    reading_retention_days: int = 90
    default_boiler_power_watts: float = 15000.0
    tado_refresh_token: str | None = None

    model_config = {"env_prefix": "MCHOME2_"}


settings = Settings()

# Overlay from settings file if it exists
if SETTINGS_FILE and Path(SETTINGS_FILE).is_file():
    with open(SETTINGS_FILE) as f:
        overrides = json.load(f)
    for key, value in overrides.items():
        if hasattr(settings, key):
            setattr(settings, key, value)


def save_settings(updates: dict) -> None:
    """Persist setting overrides to the settings file."""
    path = SETTINGS_FILE
    if not path:
        return
    existing = {}
    if Path(path).is_file():
        with open(path) as f:
            existing = json.load(f)
    existing.update(updates)
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)
