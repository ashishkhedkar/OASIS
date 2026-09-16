"""
OASIS - AIS Filtering

M4: Vessel Attribution
Filters AIS records to find vessels operating near a candidate spill origin.
"""

import pandas as pd

from src.ais.geo_utils import calculate_distance_km


def filter_nearby_vessels(
    df,
    origin_latitude,
    origin_longitude,
    radius_km=50,
):
    """
    Return AIS records within a specified radius of a candidate origin.

    Parameters
    ----------
    df : pandas.DataFrame
        Preprocessed AIS data.
    origin_latitude : float
        Latitude of the candidate spill origin.
    origin_longitude : float
        Longitude of the candidate spill origin.
    radius_km : float
        Maximum distance from the origin in kilometres.
    """

    df = df.copy()

    # Calculate each vessel observation's distance from the candidate origin.
    df["distance_km"] = calculate_distance_km(
        origin_latitude,
        origin_longitude,
        df["LAT"],
        df["LON"],
    )

    # Keep only AIS observations inside the search radius.
    nearby = df[df["distance_km"] <= radius_km].copy()

    return nearby.reset_index(drop=True)


if __name__ == "__main__":
    from src.ais.loader import load_ais_data
    from src.ais.preprocessing import preprocess_ais_data

    ais_data = load_ais_data()
    clean_data = preprocess_ais_data(ais_data)

    # Temporary test location; this will later come from M3.
    nearby_vessels = filter_nearby_vessels(
        clean_data,
        origin_latitude=18.52,
        origin_longitude=72.85,
        radius_km=50,
    )

    print("AIS filtering completed.")
    print(f"Nearby AIS records: {len(nearby_vessels)}")
    
    
    # from src.ais.geo_utils import calculate_distance_km
    # That means geo_utils.py needs to contain the distance function.