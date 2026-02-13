import logging
import os
import subprocess
import sys

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from mchome2.config import settings
from mchome2.schemas.setup import SetupStatus, DbCheckResponse, MigrateResponse

router = APIRouter(prefix="/api/setup", tags=["setup"])
logger = logging.getLogger(__name__)


@router.get("/status", response_model=SetupStatus)
async def get_setup_status():
    status = SetupStatus()

    # Check DB connectivity
    try:
        engine = create_async_engine(settings.database_url, echo=False)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        status.db_connected = True
        await engine.dispose()
    except Exception:
        return status

    # Check if migrations have been run (check if 'houses' table exists)
    try:
        engine = create_async_engine(settings.database_url, echo=False)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1 FROM houses LIMIT 0"))
        status.migrations_done = True
        await engine.dispose()
    except Exception:
        await engine.dispose()
        return status

    # Check if any houses exist
    try:
        engine = create_async_engine(settings.database_url, echo=False)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT COUNT(*) FROM houses"))
            count = result.scalar()
            status.houses_exist = count > 0
        await engine.dispose()
    except Exception:
        await engine.dispose()

    status.setup_complete = status.db_connected and status.migrations_done and status.houses_exist
    return status


@router.post("/check-db", response_model=DbCheckResponse)
async def check_db():
    try:
        engine = create_async_engine(settings.database_url, echo=False)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
        return DbCheckResponse(connected=True)
    except Exception as e:
        return DbCheckResponse(connected=False, error=str(e))


@router.post("/migrate", response_model=MigrateResponse)
async def run_migrate():
    try:
        env = os.environ.copy()
        env["MCHOME2_DATABASE_URL"] = settings.database_url
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
        if result.returncode == 0:
            return MigrateResponse(success=True, message="Migrations applied successfully")
        return MigrateResponse(success=False, message=result.stderr or result.stdout)
    except Exception as e:
        return MigrateResponse(success=False, message=str(e))
