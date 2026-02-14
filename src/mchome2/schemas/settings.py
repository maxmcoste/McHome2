from pydantic import BaseModel


class SettingsRead(BaseModel):
    database_url: str
    sensor_poll_interval_seconds: int
    prediction_interval_seconds: int
    prediction_horizon_minutes: int
    reading_retention_days: int
    default_boiler_power_watts: float
    tado_refresh_token: str | None = None


class SettingsUpdate(BaseModel):
    sensor_poll_interval_seconds: int | None = None
    prediction_interval_seconds: int | None = None
    prediction_horizon_minutes: int | None = None
    reading_retention_days: int | None = None
    default_boiler_power_watts: float | None = None
    tado_refresh_token: str | None = None
