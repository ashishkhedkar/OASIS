"""
OASIS - AIS Preprocessing

M4: Vessel Attribution
Cleans and prepares AIS records for vessel analysis.
"""

import pandas as pd

from src.ais.loader import load_ais_data


def preprocess_ais_data(df):
    """Clean AIS records and prepare them for analysis."""

    df = df.copy()

    # Convert timestamps so we can perform time-based vessel matching.
    df["BaseDateTime"] = pd.to_datetime(
        df["BaseDateTime"],
        errors="coerce",
        utc=True,
    )

    # Convert navigation fields to numeric values.
    numeric_columns = [
        "MMSI",
        "LAT",
        "LON",
        "SOG",
        "COG",
        "Heading",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove records without the information needed for attribution.
    df = df.dropna(
        subset=[
            "MMSI",
            "BaseDateTime",
            "LAT",
            "LON",
        ]
    )

    # Keep only valid geographic coordinates.
    df = df[
        df["LAT"].between(-90, 90)
        & df["LON"].between(-180, 180)
    ]

    # Sort records chronologically for later trajectory analysis.
    df = df.sort_values(
        ["MMSI", "BaseDateTime"]
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":
    ais_data = load_ais_data()
    cleaned_data = preprocess_ais_data(ais_data)

    print("AIS preprocessing completed.")
    print(f"Original records: {len(ais_data)}")
    print(f"Clean records: {len(cleaned_data)}")
    print(f"Records removed: {len(ais_data) - len(cleaned_data)}")