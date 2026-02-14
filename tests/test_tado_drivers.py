"""Tests for Tado hardware drivers."""

from unittest.mock import MagicMock, patch
import uuid

import pytest

from mchome2.hardware.tado.temperature import TadoTemperatureSensor
from mchome2.hardware.tado.boiler import TadoBoilerController
from mchome2.hardware.protocols import TemperatureSensor, BoilerController
from mchome2.hardware.registry import registry


def test_tado_drivers_conform_to_protocols():
    sensor = TadoTemperatureSensor(device_id="t1", zone_id=1, refresh_token="tok")
    assert isinstance(sensor, TemperatureSensor)

    boiler = TadoBoilerController(device_id="b1", zone_id=1, refresh_token="tok")
    assert isinstance(boiler, BoilerController)


def test_registry_creates_tado_devices():
    config = {"device_id": "t1", "zone_id": 1, "refresh_token": "tok"}
    temp = registry.create_device("temperature_sensor", "tado", config)
    assert isinstance(temp, TadoTemperatureSensor)

    config = {"device_id": "b1", "zone_id": 1, "refresh_token": "tok"}
    boiler = registry.create_device("boiler", "tado", config)
    assert isinstance(boiler, TadoBoilerController)


@pytest.mark.asyncio
@patch("mchome2.hardware.tado.temperature.get_tado_client")
async def test_tado_read_temperature(mock_get_client):
    mock_client = MagicMock()
    mock_zone_state = MagicMock()
    mock_zone_state.current_temp = 21.5
    mock_client.getZoneState.return_value = mock_zone_state
    mock_get_client.return_value = mock_client

    sensor = TadoTemperatureSensor(device_id="t1", zone_id=3, refresh_token="tok")
    temp = await sensor.read_temperature()

    assert temp == 21.5
    mock_get_client.assert_called_once_with("tok")
    mock_client.getZoneState.assert_called_once_with(3)


@pytest.mark.asyncio
@patch("mchome2.hardware.tado.boiler.get_tado_client")
async def test_tado_boiler_turn_on(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    boiler = TadoBoilerController(device_id="b1", zone_id=2, refresh_token="tok", target_temp=22.0)
    await boiler.turn_on()

    mock_client.setZoneOverlay.assert_called_once_with(2, "MANUAL", 22.0)


@pytest.mark.asyncio
@patch("mchome2.hardware.tado.boiler.get_tado_client")
async def test_tado_boiler_turn_off(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    boiler = TadoBoilerController(device_id="b1", zone_id=2, refresh_token="tok")
    await boiler.turn_off()

    mock_client.resetZoneOverlay.assert_called_once_with(2)


@pytest.mark.asyncio
@patch("mchome2.hardware.tado.boiler.get_tado_client")
async def test_tado_boiler_is_on(mock_get_client):
    mock_client = MagicMock()
    mock_zone_state = MagicMock()
    mock_get_client.return_value = mock_client

    boiler = TadoBoilerController(device_id="b1", zone_id=2, refresh_token="tok")

    # Heating is on
    mock_zone_state.heating_power_percentage = 75
    mock_client.getZoneState.return_value = mock_zone_state
    assert await boiler.is_on() is True

    # Heating is off
    mock_zone_state.heating_power_percentage = 0
    assert await boiler.is_on() is False


def test_token_injection_in_instantiate_driver():
    from mchome2.services.device_service import instantiate_driver
    from mchome2.models import Device, DeviceType

    device = Device(
        id=uuid.uuid4(),
        house_id=uuid.uuid4(),
        name="Tado Living Room",
        device_type=DeviceType.temperature_sensor,
        driver_name="tado",
        config_json={"zone_id": 1},
    )

    with patch("mchome2.config.settings") as mock_settings:
        mock_settings.tado_refresh_token = "test-token"
        with patch("mchome2.hardware.tado.temperature.get_tado_client"):
            driver = instantiate_driver(device)
            assert isinstance(driver, TadoTemperatureSensor)
            assert driver._refresh_token == "test-token"
            assert driver._zone_id == 1
