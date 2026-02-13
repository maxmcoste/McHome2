from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from mchome2.prediction.thermal_model import RoomThermalParams, euler_step
from mchome2.prediction.solar import get_solar_gain
from mchome2.prediction.pid_controller import create_pid, should_boiler_be_on


@dataclass
class PredictionInput:
    latitude: float
    longitude: float
    room_params: RoomThermalParams
    current_temp_c: float
    desired_temp_c: float
    t_outside_c: float
    windows_open: bool
    boiler_power_watts: float
    start_time: datetime
    horizon_minutes: int = 240
    step_seconds: int = 60


@dataclass
class PredictionStep:
    time: str  # ISO format
    boiler_on: bool
    expected_temp: float

    def to_dict(self) -> dict:
        return {"time": self.time, "boiler_on": self.boiler_on, "expected_temp": round(self.expected_temp, 2)}


def run_prediction(inp: PredictionInput) -> list[PredictionStep]:
    """Run thermal prediction over the horizon.

    Returns a list of PredictionStep for each time step.
    """
    pid = create_pid(inp.desired_temp_c)
    steps: list[PredictionStep] = []
    t_room = inp.current_temp_c
    current_time = inp.start_time
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    total_steps = (inp.horizon_minutes * 60) // inp.step_seconds

    for _ in range(total_steps):
        # Decide boiler state
        boiler_on = should_boiler_be_on(pid, t_room)

        # Calculate solar gain at current time
        solar_gain = get_solar_gain(
            inp.latitude,
            inp.longitude,
            current_time,
            inp.room_params.window_area_m2,
            inp.room_params.orientation,
        )

        # Record this step
        steps.append(PredictionStep(
            time=current_time.isoformat(),
            boiler_on=boiler_on,
            expected_temp=round(t_room, 2),
        ))

        # Euler integration step
        t_room = euler_step(
            t_room=t_room,
            t_outside=inp.t_outside_c,
            params=inp.room_params,
            boiler_on=boiler_on,
            boiler_power_watts=inp.boiler_power_watts,
            solar_gain_watts=solar_gain,
            windows_open=inp.windows_open,
            dt_seconds=inp.step_seconds,
        )

        current_time += timedelta(seconds=inp.step_seconds)

    return steps
