class SimulatedWindowSensor:
    def __init__(self, device_id: str = "sim-window-001", is_open: bool = False) -> None:
        self._device_id = device_id
        self._is_open = is_open

    async def read_is_open(self) -> bool:
        return self._is_open

    def device_id(self) -> str:
        return self._device_id

    def set_open(self, is_open: bool) -> None:
        self._is_open = is_open
