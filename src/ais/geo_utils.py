"""
OASIS - AIS Geographic Utilities

M4: Vessel Attribution
Provides geographic distance calculations for vessel filtering.
"""

import numpy as np


EARTH_RADIUS_KM = 6371.0


def calculate_distance_km(
    latitude1,
    longitude1,
    latitude2,
    longitude2,
):
    """
    Calculate great-circle distance between two geographic points.

    latitude2 and longitude2 can be individual values or pandas Series.
    Returns distance in kilometres.
    """

    # Convert coordinates from degrees to radians for the Haversine formula.
    lat1 = np.radians(latitude1)
    lon1 = np.radians(longitude1)
    lat2 = np.radians(latitude2)
    lon2 = np.radians(longitude2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Haversine formula calculates distance along Earth's surface.
    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(delta_lon / 2) ** 2
    )

    c = 2 * np.arctan2(
        np.sqrt(a),
        np.sqrt(1 - a),
    )

    return EARTH_RADIUS_KM * c


if __name__ == "__main__":
    distance = calculate_distance_km(
        18.52,
        72.85,
        18.62,
        72.95,
    )

    print(f"Distance: {distance:.2f} km")