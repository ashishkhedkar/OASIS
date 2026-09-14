from src.drift.currents import get_current
from src.drift.wind import get_wind
from src.drift.trajectory import generate_backtrack_trajectory
from src.drift.confidence import calculate_confidence


def predict_origins(
    latitude,
    longitude,
    timestamp,
    total_hours=6,
    step_hours=1,
):
    """
    Estimate candidate spill origins from an
    observed spill location and timestamp.
    """

    current = get_current(
        latitude,
        longitude,
        timestamp,
    )

    wind = get_wind(
        latitude,
        longitude,
        timestamp,
    )

    trajectory = generate_backtrack_trajectory(
        latitude=latitude,
        longitude=longitude,
        current=current,
        wind=wind,
        total_hours=total_hours,
        step_hours=step_hours,
    )

    origins = []

    for point in trajectory[1:]:
        confidence = calculate_confidence(
            point["hours_back"],
            max_backtrack_hours=total_hours,
        )

        origins.append(
            {
                "latitude": point["latitude"],
                "longitude": point["longitude"],
                "hours_back": point["hours_back"],
                "confidence": confidence,
            }
        )

    return origins


if __name__ == "__main__":
    origins = predict_origins(
        latitude=18.52,
        longitude=72.85,
        timestamp="2019-04-18T12:00:00",
    )

    print("Candidate origins:")

    for origin in origins:
        print(
            f"{origin['hours_back']}h back → "
            f"{origin['latitude']:.6f}, "
            f"{origin['longitude']:.6f} "
            f"(confidence: "
            f"{origin['confidence']:.2f})"
        )