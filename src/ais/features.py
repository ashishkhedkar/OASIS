"""
OASIS - AIS Feature Extraction

M4: Vessel Attribution
Calculates useful evidence features for each AIS record
relative to a suspected oil-spill origin.
"""

import pandas as pd

from src.ais.geo_utils import calculate_distance_km


def calculate_attribution_features(
    df,
    origin_latitude,
    origin_longitude,
    origin_timestamp,
):
    """
    Calculate spatial and temporal features for AIS records.

    Parameters
    ----------
    df : pandas.DataFrame
        Filtered AIS records.
    origin_latitude : float
        Latitude of the suspected spill origin.
    origin_longitude : float
        Longitude of the suspected spill origin.
    origin_timestamp : str
        Timestamp of the suspected spill origin.

    Returns
    -------
    pandas.DataFrame
        AIS records with attribution-related features.
    """

    df = df.copy()

    # Convert AIS timestamps and the suspected origin time
    # into datetime values so we can calculate time differences.
    df["BaseDateTime"] = pd.to_datetime(
        df["BaseDateTime"],
        errors="coerce",
    )

    origin_time = pd.to_datetime(
        origin_timestamp,
        errors="coerce",
    )

    if pd.isna(origin_time):
        raise ValueError("Invalid origin timestamp.")

    # Calculate geographic distance between every AIS position
    # and the suspected spill origin.
    df["distance_km"] = df.apply(
        lambda row: calculate_distance_km(
            origin_latitude,
            origin_longitude,
            row["LAT"],
            row["LON"],
        ),
        axis=1,
    )

    # Calculate how many hours separate each AIS observation
    # from the suspected spill time.
    df["time_difference_hours"] = (
        (df["BaseDateTime"] - origin_time)
        .abs()
        .dt.total_seconds()
        / 3600
    )

    # Keep the movement information supplied by AIS.
    df["SOG"] = pd.to_numeric(df["SOG"], errors="coerce")
    df["COG"] = pd.to_numeric(df["COG"], errors="coerce")
    df["Heading"] = pd.to_numeric(df["Heading"], errors="coerce")

    return df


if __name__ == "__main__":
    print("AIS feature extraction module ready.")