from mchome2.prediction.thermal_model import RoomThermalParams, compute_heat_loss, euler_step


def test_thermal_resistance_increases_with_insulation():
    low = RoomThermalParams(volume_m3=50, insulation_factor=0.1, window_area_m2=2, orientation="S")
    high = RoomThermalParams(volume_m3=50, insulation_factor=0.9, window_area_m2=2, orientation="S")
    assert high.thermal_resistance > low.thermal_resistance


def test_heat_loss_positive_when_room_warmer():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    loss = compute_heat_loss(t_room=22.0, t_outside=5.0, r_thermal=params.thermal_resistance, windows_open=False)
    assert loss > 0


def test_heat_loss_increases_with_open_windows():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    loss_closed = compute_heat_loss(22, 5, params.thermal_resistance, windows_open=False)
    loss_open = compute_heat_loss(22, 5, params.thermal_resistance, windows_open=True)
    assert loss_open > loss_closed


def test_euler_step_heats_when_boiler_on():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    new_temp = euler_step(
        t_room=18.0, t_outside=5.0, params=params,
        boiler_on=True, boiler_power_watts=15000,
        solar_gain_watts=0, windows_open=False, dt_seconds=60,
    )
    assert new_temp > 18.0


def test_euler_step_cools_when_boiler_off_and_cold_outside():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    new_temp = euler_step(
        t_room=22.0, t_outside=5.0, params=params,
        boiler_on=False, boiler_power_watts=15000,
        solar_gain_watts=0, windows_open=False, dt_seconds=60,
    )
    assert new_temp < 22.0


def test_solar_gain_increases_temperature():
    params = RoomThermalParams(volume_m3=50, insulation_factor=0.5, window_area_m2=2, orientation="S")
    temp_no_solar = euler_step(
        t_room=20.0, t_outside=20.0, params=params,
        boiler_on=False, boiler_power_watts=0,
        solar_gain_watts=0, windows_open=False, dt_seconds=60,
    )
    temp_with_solar = euler_step(
        t_room=20.0, t_outside=20.0, params=params,
        boiler_on=False, boiler_power_watts=0,
        solar_gain_watts=500, windows_open=False, dt_seconds=60,
    )
    assert temp_with_solar > temp_no_solar
