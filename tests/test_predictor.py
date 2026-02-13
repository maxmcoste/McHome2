from datetime import datetime, timezone

from mchome2.prediction.thermal_model import RoomThermalParams
from mchome2.prediction.predictor import PredictionInput, run_prediction


def test_prediction_generates_steps():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    inp = PredictionInput(
        latitude=41.9,
        longitude=12.5,
        room_params=params,
        current_temp_c=18.0,
        desired_temp_c=22.0,
        t_outside_c=5.0,
        windows_open=False,
        boiler_power_watts=15000,
        start_time=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
        horizon_minutes=30,
        step_seconds=60,
    )
    steps = run_prediction(inp)
    assert len(steps) == 30  # 30 minutes / 1 minute steps
    assert all(hasattr(s, "boiler_on") for s in steps)
    assert all(hasattr(s, "expected_temp") for s in steps)


def test_prediction_heats_towards_setpoint():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    inp = PredictionInput(
        latitude=41.9,
        longitude=12.5,
        room_params=params,
        current_temp_c=15.0,
        desired_temp_c=22.0,
        t_outside_c=5.0,
        windows_open=False,
        boiler_power_watts=15000,
        start_time=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
        horizon_minutes=120,
        step_seconds=60,
    )
    steps = run_prediction(inp)
    # Temperature should increase over time toward setpoint
    assert steps[-1].expected_temp > steps[0].expected_temp
    # The boiler should be on initially since room is cold
    assert steps[0].boiler_on is True


def test_prediction_boiler_off_when_warm():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    inp = PredictionInput(
        latitude=41.9,
        longitude=12.5,
        room_params=params,
        current_temp_c=25.0,
        desired_temp_c=20.0,
        t_outside_c=10.0,
        windows_open=False,
        boiler_power_watts=15000,
        start_time=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
        horizon_minutes=30,
        step_seconds=60,
    )
    steps = run_prediction(inp)
    # Room is warmer than desired, boiler should be off
    assert steps[0].boiler_on is False


def test_prediction_to_dict():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    inp = PredictionInput(
        latitude=41.9,
        longitude=12.5,
        room_params=params,
        current_temp_c=20.0,
        desired_temp_c=22.0,
        t_outside_c=5.0,
        windows_open=False,
        boiler_power_watts=15000,
        start_time=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
        horizon_minutes=5,
        step_seconds=60,
    )
    steps = run_prediction(inp)
    d = steps[0].to_dict()
    assert "time" in d
    assert "boiler_on" in d
    assert "expected_temp" in d
