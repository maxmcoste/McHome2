"""Tado boiler controller driver."""

import asyncio

from mchome2.hardware.tado.client import get_tado_client


class TadoBoilerController:
    def __init__(
        self,
        device_id: str,
        zone_id: int,
        refresh_token: str,
        target_temp: float = 25.0,
    ) -> None:
        self._device_id = device_id
        self._zone_id = zone_id
        self._refresh_token = refresh_token
        self._target_temp = target_temp

    async def turn_on(self) -> None:
        client = get_tado_client(self._refresh_token)
        await asyncio.to_thread(
            client.setZoneOverlay,
            self._zone_id,
            "MANUAL",
            self._target_temp,
        )

    async def turn_off(self) -> None:
        client = get_tado_client(self._refresh_token)
        await asyncio.to_thread(client.resetZoneOverlay, self._zone_id)

    async def is_on(self) -> bool:
        client = get_tado_client(self._refresh_token)
        zone_state = await asyncio.to_thread(client.getZoneState, self._zone_id)
        return (zone_state.heating_power_percentage or 0) > 0

    def device_id(self) -> str:
        return self._device_id
