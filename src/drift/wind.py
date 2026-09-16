def get_wind(latitude, longitude, timestamp):
    """
    Return wind velocity at a given location and time.

    Returns:
        Dictionary containing east and north
        wind components in m/s.
    """

    return {
        "east_mps": 2.0,
        "north_mps": 0.5,
    }


if __name__ == "__main__":
    wind = get_wind(
        latitude=18.52,
        longitude=72.85,
        timestamp="2019-04-18T12:00:00",
    )

    print("Wind data:")
    print(wind)