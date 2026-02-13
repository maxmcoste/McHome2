import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mchome2.config import settings
from mchome2.models import House, Room, Prediction, DeviceType, BoilerAction
from mchome2.prediction.thermal_model import RoomThermalParams
from mchome2.prediction.predictor import PredictionInput, run_prediction
from mchome2.services import reading_service, device_service, room_service


async def run_house_predictions(session: AsyncSession, house_id: uuid.UUID) -> list[Prediction]:
    """Run predictions for all rooms in a house and decide boiler action."""
    house = await session.get(House, house_id)
    if not house:
        return []

    rooms_result = await session.execute(
        select(Room).where(Room.house_id == house_id)
    )
    rooms = list(rooms_result.scalars().all())
    if not rooms:
        return []

    now = datetime.now(timezone.utc)
    predictions = []
    any_room_needs_heat = False

    for room in rooms:
        # Get current temperature
        current_temp = await reading_service.get_latest_room_temperature(session, room.id)
        if current_temp is None:
            current_temp = 18.0  # default assumption

        # Get desired temperature from schedule
        desired_temp = await room_service.get_desired_temp(
            session, room.id, now.weekday(), now.time()
        )
        if desired_temp is None:
            desired_temp = 20.0  # default

        # Get window status
        windows_open, _ = await reading_service.get_room_window_status(session, room.id)

        # Outside temperature approximation (could be enhanced with weather API)
        t_outside = 5.0

        room_params = RoomThermalParams(
            volume_m3=room.volume_m3,
            insulation_factor=room.insulation_factor,
            window_area_m2=room.window_area_m2,
            orientation=room.orientation,
        )

        inp = PredictionInput(
            latitude=house.latitude,
            longitude=house.longitude,
            room_params=room_params,
            current_temp_c=current_temp,
            desired_temp_c=desired_temp,
            t_outside_c=t_outside,
            windows_open=windows_open > 0,
            boiler_power_watts=settings.default_boiler_power_watts,
            start_time=now,
            horizon_minutes=settings.prediction_horizon_minutes,
        )

        steps = run_prediction(inp)

        # Check if the first step says boiler should be on
        if steps and steps[0].boiler_on:
            any_room_needs_heat = True

        prediction = Prediction(
            house_id=house_id,
            room_id=room.id,
            schedule_json=[s.to_dict() for s in steps],
            horizon_minutes=settings.prediction_horizon_minutes,
        )
        session.add(prediction)
        predictions.append(prediction)

    # Execute boiler command based on aggregate decision
    boiler_devices = await device_service.get_active_devices(session, house_id, DeviceType.boiler)
    for boiler_dev in boiler_devices:
        driver = device_service.instantiate_driver(boiler_dev)
        current_state = await driver.is_on()

        if any_room_needs_heat and not current_state:
            await driver.turn_on()
            await reading_service.record_boiler_event(
                session, boiler_dev.id, house_id, BoilerAction.on, "prediction"
            )
        elif not any_room_needs_heat and current_state:
            await driver.turn_off()
            await reading_service.record_boiler_event(
                session, boiler_dev.id, house_id, BoilerAction.off, "prediction"
            )

    await session.commit()
    for p in predictions:
        await session.refresh(p)
    return predictions


async def get_latest_prediction(session: AsyncSession, room_id: uuid.UUID) -> Prediction | None:
    result = await session.execute(
        select(Prediction)
        .where(Prediction.room_id == room_id)
        .order_by(Prediction.predicted_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
