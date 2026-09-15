"""
OASIS - Geospatial Utilities

M1: Data Collection
Basic utilities for handling geographic coordinates
used by satellite, ocean, wind, and AIS data.
"""

from math import radians, sin, cos, sqrt, atan2


def validate_coordinates(latitude, longitude):
    """Check whether latitude and longitude are valid."""

    if not -90 <= latitude <= 90:
        return False

    if not -180 <= longitude <= 180:
        return False

    return True


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate approximate distance between two coordinates
    using the Haversine formula.

    Returns:
        Distance in kilometers.
    """

    earth_radius = 6371.0

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


if __name__ == "__main__":
    latitude = 13.2282
    longitude = 80.3633

    if validate_coordinates(latitude, longitude):
        print("Coordinates are valid.")
        print(f"Test location: {latitude}, {longitude}")