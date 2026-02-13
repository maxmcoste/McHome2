import pytest

from mchome2.hardware.simulator.temperature import SimulatedTemperatureSensor
from mchome2.hardware.simulator.window import SimulatedWindowSensor
from mchome2.hardware.simulator.boiler import SimulatedBoilerController
from mchome2.hardware.protocols import TemperatureSensor, WindowSensor, BoilerController
from mchome2.hardware.registry import registry


@pytest.mark.asyncio
async def test_simulated_temperature_sensor():
    sensor = SimulatedTemperatureSensor(device_id="test-temp", base_temp=21.0, variance=0.5)
    temp = await sensor.read_temperature()
    assert 20.5 <= temp <= 21.5
    assert sensor.device_id() == "test-temp"


@pytest.mark.asyncio
async def test_simulated_temperature_sensor_set_base():
    sensor = SimulatedTemperatureSensor(base_temp=20.0, variance=0.0)
    sensor.set_base_temp(25.0)
    temp = await sensor.read_temperature()
    assert temp == 25.0


@pytest.mark.asyncio
async def test_simulated_window_sensor():
    sensor = SimulatedWindowSensor(device_id="test-win")
    assert await sensor.read_is_open() is False
    sensor.set_open(True)
    assert await sensor.read_is_open() is True
    assert sensor.device_id() == "test-win"


@pytest.mark.asyncio
async def test_simulated_boiler_controller():
    boiler = SimulatedBoilerController(device_id="test-boiler")
    assert await boiler.is_on() is False
    await boiler.turn_on()
    assert await boiler.is_on() is True
    await boiler.turn_off()
    assert await boiler.is_on() is False
    assert boiler.device_id() == "test-boiler"


def test_simulators_conform_to_protocols():
    assert isinstance(SimulatedTemperatureSensor(), TemperatureSensor)
    assert isinstance(SimulatedWindowSensor(), WindowSensor)
    assert isinstance(SimulatedBoilerController(), BoilerController)


def test_registry_creates_simulator_devices():
    temp = registry.create_device("temperature_sensor", "simulator", {"device_id": "t1"})
    assert isinstance(temp, SimulatedTemperatureSensor)

    win = registry.create_device("window_sensor", "simulator", {"device_id": "w1"})
    assert isinstance(win, SimulatedWindowSensor)

    boiler = registry.create_device("boiler", "simulator", {"device_id": "b1"})
    assert isinstance(boiler, SimulatedBoilerController)


def test_registry_raises_for_unknown_driver():
    with pytest.raises(ValueError, match="No driver registered"):
        registry.create_device("temperature_sensor", "nonexistent")
