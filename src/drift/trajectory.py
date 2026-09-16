from src.drift.coordinate_utils import move_point
from src.drift.drift_model import (
    calculate_drift_velocity,
    displacement_after_hours,
)


def generate_backtrack_trajectory(
    latitude,
    longitude,
    current,
    wind,
    total_hours,
    step_hours=1,
):
    """
    Generate points along the estimated spill path
    while moving backwards in time.
    """

    velocity = calculate_drift_velocity(
        current,
        wind,
    )

    trajectory = [
        {
            "latitude": latitude,
            "longitude": longitude,
            "hours_back": 0,
        }
    ]

    steps = int(total_hours / step_hours)

    for step in range(1, steps + 1):
        hours_back = step * step_hours

        displacement = displacement_after_hours(
            velocity,
            hours_back,
        )

        # Reverse the forward drift to backtrack the spill.
        point_lat, point_lon = move_point(
            latitude,
            longitude,
            north_km=-displacement["north_km"],
            east_km=-displacement["east_km"],
        )

        trajectory.append(
            {
                "latitude": point_lat,
                "longitude": point_lon,
                "hours_back": hours_back,
            }
        )

    return trajectory


if __name__ == "__main__":
    current = {
        "east_mps": 0.4,
        "north_mps": 0.1,
    }

    wind = {
        "east_mps": 2.0,
        "north_mps": 0.5,
    }

    trajectory = generate_backtrack_trajectory(
        latitude=18.52,
        longitude=72.85,
        current=current,
        wind=wind,
        total_hours=6,
        step_hours=1,
    )

    print("Backtracked trajectory:")

    for point in trajectory:
        print(
            f"{point['hours_back']}h back: "
            f"{point['latitude']:.6f}, "
            f"{point['longitude']:.6f}"
        )