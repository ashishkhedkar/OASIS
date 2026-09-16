from src.drift.coordinate_utils import move_point
from src.drift.drift_model import (
    calculate_drift_velocity,
    displacement_after_hours,
)


def backtrack_spill(
    latitude,
    longitude,
    current,
    wind,
    hours,
):
    """
    Estimate where the spill originated by moving
    backwards from its observed location.
    """

    velocity = calculate_drift_velocity(
        current,
        wind,
    )

    displacement = displacement_after_hours(
        velocity,
        hours,
    )

    # Reverse the displacement to travel back toward the origin.
    origin_lat, origin_lon = move_point(
        latitude,
        longitude,
        north_km=-displacement["north_km"],
        east_km=-displacement["east_km"],
    )

    return origin_lat, origin_lon


if __name__ == "__main__":
    spill_latitude = 18.52
    spill_longitude = 72.85

    current = {
        "east_mps": 0.4,
        "north_mps": 0.1,
    }

    wind = {
        "east_mps": 2.0,
        "north_mps": 0.5,
    }

    origin_lat, origin_lon = backtrack_spill(
        latitude=spill_latitude,
        longitude=spill_longitude,
        current=current,
        wind=wind,
        hours=2,
    )

    print("Observed spill:")
    print(
        f"{spill_latitude:.6f}, "
        f"{spill_longitude:.6f}"
    )

    print("Estimated origin:")
    print(
        f"{origin_lat:.6f}, "
        f"{origin_lon:.6f}"
    )