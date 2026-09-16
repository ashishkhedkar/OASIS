from datetime import datetime, timedelta

from src.drift.coordinate_utils import move_point
from src.drift.drift_model import (
    calculate_drift_velocity,
    displacement_after_hours,
)
from src.drift.currents import get_current
from src.drift.wind import get_wind


def generate_backtrack_trajectory(
    latitude,
    longitude,
    timestamp,
    total_hours,
    step_hours=1,
):
    """
    Generate points along the estimated spill path
    while moving backwards in time.

    Real ocean-current and wind data are fetched
    for each backtracking step.
    """

    trajectory = [
        {
            "latitude": latitude,
            "longitude": longitude,
            "hours_back": 0,
        }
    ]

    current_latitude = latitude
    current_longitude = longitude

    current_time = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    steps = int(total_hours / step_hours)

    for step in range(1, steps + 1):
        hours_back = step * step_hours

        backtrack_time = current_time - timedelta(
            hours=hours_back
        )

        time_string = backtrack_time.isoformat()

        current = get_current(
            current_latitude,
            current_longitude,
            time_string,
        )

        wind = get_wind(
            current_latitude,
            current_longitude,
            time_string,
        )

        velocity = calculate_drift_velocity(
            current,
            wind,
        )

        displacement = displacement_after_hours(
            velocity,
            step_hours,
        )

        # Reverse the forward drift to backtrack the spill.
        current_latitude, current_longitude = move_point(
            current_latitude,
            current_longitude,
            north_km=-displacement["north_km"],
            east_km=-displacement["east_km"],
        )

        trajectory.append(
            {
                "latitude": current_latitude,
                "longitude": current_longitude,
                "hours_back": hours_back,
            }
        )

    return trajectory


if __name__ == "__main__":
    trajectory = generate_backtrack_trajectory(
        latitude=13.2282,
        longitude=80.3633,
        timestamp="2017-01-29T12:00:00",
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