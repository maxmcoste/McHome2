from pydantic import BaseModel


class SetupStatus(BaseModel):
    db_connected: bool = False
    migrations_done: bool = False
    houses_exist: bool = False
    setup_complete: bool = False


class DbCheckResponse(BaseModel):
    connected: bool
    error: str | None = None


class MigrateResponse(BaseModel):
    success: bool
    message: str
