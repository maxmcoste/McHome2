import math
from datetime import datetime

from pysolar.solar import get_altitude, get_azimuth


def get_solar_gain(
    latitude: float,
    longitude: float,
    dt: datetime,
    window_area_m2: float,
    orientation: str,
    transmittance: float = 0.6,
) -> float:
    """Calculate solar heat gain through windows in watts.

    Args:
        latitude: House latitude
        longitude: House longitude
        dt: Datetime (timezone-aware)
        window_area_m2: Window area in m2
        orientation: Room orientation (N, S, E, W, NE, NW, SE, SW)
        transmittance: Glass transmittance factor (0-1)

    Returns:
        Solar gain in watts (0 if sun is below horizon)
    """
    altitude = get_altitude(latitude, longitude, dt)
    if altitude <= 0:
        return 0.0

    azimuth = get_azimuth(latitude, longitude, dt)

    # Map orientation to azimuth angle
    orientation_azimuths = {
        "N": 0, "NE": 45, "E": 90, "SE": 135,
        "S": 180, "SW": 225, "W": 270, "NW": 315,
    }
    wall_azimuth = orientation_azimuths.get(orientation, 180)

    # Angle of incidence: angle between sun direction and window normal
    sun_az_rad = math.radians(azimuth)
    wall_az_rad = math.radians(wall_azimuth)
    alt_rad = math.radians(altitude)

    cos_incidence = (
        math.sin(alt_rad) * math.cos(0)  # vertical window
        + math.cos(alt_rad) * math.sin(math.pi / 2) * math.cos(sun_az_rad - wall_az_rad)
    )
    cos_incidence = max(0, cos_incidence)

    # Direct normal irradiance approximation (W/m2)
    # Simple model: ~1000 W/m2 at sea level, reduced by atmospheric path length
    air_mass = 1 / (math.sin(alt_rad) + 0.50572 * (6.07995 + altitude) ** -1.6364)
    dni = 1353 * 0.7 ** (air_mass ** 0.678)  # Meinel model

    solar_gain = dni * cos_incidence * window_area_m2 * transmittance
    return max(0, solar_gain)
