from simple_pid import PID


def create_pid(setpoint: float, kp: float = 1.0, ki: float = 0.1, kd: float = 0.05) -> PID:
    """Create a PID controller for boiler control.

    The PID output is used to decide on/off:
    - Positive output -> boiler should be ON (room is too cold)
    - Negative output -> boiler should be OFF (room is warm enough)
    """
    pid = PID(kp, ki, kd, setpoint=setpoint)
    pid.output_limits = (-1, 1)
    return pid


def should_boiler_be_on(pid: PID, current_temp: float) -> bool:
    """Use PID controller to decide if the boiler should be on.

    Returns True if the boiler should be on.
    """
    output = pid(current_temp)
    # Positive output means we need heating
    return output > 0
