import logging
from contextlib import asynccontextmanager
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from mchome2.config import settings
from mchome2.api import houses, rooms, devices, readings, predictions
from mchome2.api import setup, settings as settings_api, dashboard
from mchome2.scheduler.tasks import poll_sensors, run_predictions, cleanup_old_readings

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(poll_sensors, "interval", seconds=settings.sensor_poll_interval_seconds, id="poll_sensors")
    scheduler.add_job(run_predictions, "interval", seconds=settings.prediction_interval_seconds, id="run_predictions")
    scheduler.add_job(cleanup_old_readings, "cron", hour=3, minute=0, id="cleanup_old_readings")
    scheduler.start()
    logger.info("Scheduler started")
    yield
    scheduler.shutdown()
    logger.info("Scheduler stopped")


def create_app() -> FastAPI:
    app = FastAPI(title="McHome2", version="0.1.0", lifespan=lifespan)

    # API routers
    app.include_router(setup.router)
    app.include_router(settings_api.router)
    app.include_router(dashboard.router)
    app.include_router(houses.router)
    app.include_router(rooms.router)
    app.include_router(devices.router)
    app.include_router(readings.router)
    app.include_router(predictions.router)

    # SPA static files (only if built frontend exists)
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="static-assets")

    # SPA catch-all: serve index.html for any non-API route
    index_html = STATIC_DIR / "index.html"

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # Don't serve SPA for API routes
        if full_path.startswith("api/"):
            return None
        if index_html.is_file():
            return FileResponse(str(index_html))
        return {"message": "McHome2 API is running. Frontend not built yet."}

    return app


app = create_app()
