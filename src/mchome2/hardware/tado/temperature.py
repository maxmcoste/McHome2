"""Tado temperature sensor driver."""

import asyncio

from mchome2.hardware.tado.client import get_tado_client


class TadoTemperatureSensor:
    def __init__(self, device_id: str, zone_id: int, refresh_token: str) -> None:
        self._device_id = device_id
        self._zone_id = zone_id
        self._refresh_token = refresh_token

    async def read_temperature(self) -> float:
        client = get_tado_client(self._refresh_token)
        zone_state = await asyncio.to_thread(client.getZoneState, self._zone_id)
        return zone_state.current_temp

    def device_id(self) -> str:
        return self._device_id
