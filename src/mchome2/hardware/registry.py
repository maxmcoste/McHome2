from typing import Any


class DeviceRegistry:
    def __init__(self) -> None:
        self._drivers: dict[tuple[str, str], type] = {}

    def register_driver(self, device_type: str, driver_name: str, cls: type) -> None:
        self._drivers[(device_type, driver_name)] = cls

    def create_device(self, device_type: str, driver_name: str, config: dict[str, Any] | None = None) -> Any:
        key = (device_type, driver_name)
        if key not in self._drivers:
            raise ValueError(f"No driver registered for ({device_type}, {driver_name})")
        cls = self._drivers[key]
        return cls(**(config or {}))

    def list_drivers(self) -> list[tuple[str, str]]:
        return list(self._drivers.keys())


registry = DeviceRegistry()


def _register_simulators() -> None:
    from mchome2.hardware.simulator.temperature import SimulatedTemperatureSensor
    from mchome2.hardware.simulator.window import SimulatedWindowSensor
    from mchome2.hardware.simulator.boiler import SimulatedBoilerController

    registry.register_driver("temperature_sensor", "simulator", SimulatedTemperatureSensor)
    registry.register_driver("window_sensor", "simulator", SimulatedWindowSensor)
    registry.register_driver("boiler", "simulator", SimulatedBoilerController)


def _register_tado() -> None:
    from mchome2.hardware.tado.temperature import TadoTemperatureSensor
    from mchome2.hardware.tado.boiler import TadoBoilerController

    registry.register_driver("temperature_sensor", "tado", TadoTemperatureSensor)
    registry.register_driver("boiler", "tado", TadoBoilerController)


_register_simulators()
_register_tado()
