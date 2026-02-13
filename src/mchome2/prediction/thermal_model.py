from dataclasses import dataclass


@dataclass
class RoomThermalParams:
    volume_m3: float
    insulation_factor: float  # 0 (no insulation) to 1 (perfect insulation)
    window_area_m2: float
    orientation: str

    @property
    def thermal_resistance(self) -> float:
        """R_thermal in K/W. Higher insulation = higher resistance = less heat loss."""
        # Base R value scales with volume (larger rooms have more wall area)
        # insulation_factor 0 -> R=0.001 (very leaky), 1 -> R=0.01 (well insulated)
        base_r = 0.001 + 0.009 * self.insulation_factor
        # Scale with volume: smaller rooms lose heat faster per unit volume
        return base_r * (self.volume_m3 / 50.0)

    @property
    def thermal_capacitance(self) -> float:
        """C_thermal in J/K. Air + furniture thermal mass."""
        # Air: ~1200 J/(m3*K), furniture adds ~2x
        return self.volume_m3 * 1200 * 2


def compute_heat_loss(t_room: float, t_outside: float, r_thermal: float, windows_open: bool) -> float:
    """Heat loss rate in watts. Positive = room losing heat."""
    r = r_thermal
    if windows_open:
        r *= 0.1  # Windows open: 10x more heat loss
    return (t_room - t_outside) / r


def euler_step(
    t_room: float,
    t_outside: float,
    params: RoomThermalParams,
    boiler_on: bool,
    boiler_power_watts: float,
    solar_gain_watts: float,
    windows_open: bool,
    dt_seconds: float = 60.0,
) -> float:
    """Euler integration step: compute new room temperature after dt_seconds.

    Returns:
        New room temperature in Celsius.
    """
    q_loss = compute_heat_loss(t_room, t_outside, params.thermal_resistance, windows_open)
    q_boiler = boiler_power_watts if boiler_on else 0.0
    q_solar = solar_gain_watts

    # Net heat flow into the room (watts)
    q_net = q_boiler + q_solar - q_loss

    # Temperature change: dT = Q_net * dt / C
    dt_temp = q_net * dt_seconds / params.thermal_capacitance

    return t_room + dt_temp
