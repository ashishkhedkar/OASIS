WINDAGE_COEFFICIENT = 0.03


def calculate_drift_velocity(current, wind):
    """
    Combine ocean current and wind to estimate
    effective oil drift velocity.

    Args:
        current: Dictionary with east_mps and north_mps.
        wind: Dictionary with east_mps and north_mps.

    Returns:
        Dictionary containing effective drift velocity.
    """

    east_velocity = (
        current["east_mps"]
        + WINDAGE_COEFFICIENT * wind["east_mps"]
    )

    north_velocity = (
        current["north_mps"]
        + WINDAGE_COEFFICIENT * wind["north_mps"]
    )

    return {
        "east_mps": east_velocity,
        "north_mps": north_velocity,
    }


def displacement_after_hours(velocity, hours):
    """
    Calculate north/east displacement after a
    given amount of time.

    Returns:
        Displacement in kilometers.
    """

    seconds = hours * 3600

    east_km = (
        velocity["east_mps"] * seconds / 1000
    )

    north_km = (
        velocity["north_mps"] * seconds / 1000
    )

    return {
        "east_km": east_km,
        "north_km": north_km,
    }


if __name__ == "__main__":
    current = {
        "east_mps": 0.4,
        "north_mps": 0.1,
    }

    wind = {
        "east_mps": 2.0,
        "north_mps": 0.5,
    }

    velocity = calculate_drift_velocity(
        current,
        wind,
    )

    displacement = displacement_after_hours(
        velocity,
        hours=2,
    )

    print("Effective drift velocity:")
    print(velocity)

    print("Displacement after 2 hours:")
    print(displacement)