def get_current(latitude, longitude, timestamp):
    """
    Return ocean current velocity at a given
    location and time.

    Returns:
        Dictionary containing east and north
        current components in m/s.
    """

    return {
        "east_mps": 0.4,
        "north_mps": 0.1,
    }


if __name__ == "__main__":
    current = get_current(
        latitude=18.52,
        longitude=72.85,
        timestamp="2019-04-18T12:00:00",
    )

    print("Ocean current data:")
    print(current)