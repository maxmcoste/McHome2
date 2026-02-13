import random


class SimulatedTemperatureSensor:
    def __init__(self, device_id: str = "sim-temp-001", base_temp: float = 20.0, variance: float = 0.5) -> None:
        self._device_id = device_id
        self._base_temp = base_temp
        self._variance = variance

    async def read_temperature(self) -> float:
        return self._base_temp + random.uniform(-self._variance, self._variance)

    def device_id(self) -> str:
        return self._device_id

    def set_base_temp(self, temp: float) -> None:
        self._base_temp = temp
