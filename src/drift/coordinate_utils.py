import math


EARTH_RADIUS_KM = 6371.0


def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2,
):
    """
    Calculate the distance between two geographic coordinates.

    Returns:
        Distance in kilometers.
    """

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return EARTH_RADIUS_KM * c


def move_point(
    latitude,
    longitude,
    north_km,
    east_km,
):
    """
    Move a geographic point by a specified
    distance north/south and east/west.

    Returns:
        New latitude and longitude.
    """

    latitude_change = north_km / 111.0

    longitude_scale = 111.0 * math.cos(
        math.radians(latitude)
    )

    longitude_change = east_km / longitude_scale

    new_latitude = latitude + latitude_change
    new_longitude = longitude + longitude_change

    return new_latitude, new_longitude

if __name__ == "__main__":
    distance = haversine_distance(
        18.52,
        72.85,
        18.60,
        72.85,
    )

    print(f"Distance: {distance:.2f} km")

    new_lat, new_lon = move_point(
        18.52,
        72.85,
        north_km=10,
        east_km=5,
    )

    print(
        f"New position: "
        f"{new_lat:.6f}, {new_lon:.6f}"
    )