class SimulatedBoilerController:
    def __init__(self, device_id: str = "sim-boiler-001") -> None:
        self._device_id = device_id
        self._is_on = False

    async def turn_on(self) -> None:
        self._is_on = True

    async def turn_off(self) -> None:
        self._is_on = False

    async def is_on(self) -> bool:
        return self._is_on

    def device_id(self) -> str:
        return self._device_id
