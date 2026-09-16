"""
OASIS - AIS Evidence Scoring

M4: Vessel Attribution
Converts AIS features into an evidence score for each vessel.
"""

import pandas as pd


# Maximum values used to normalize the evidence features.
# These are MVP assumptions and can be tuned after testing.
MAX_DISTANCE_KM = 10.0
MAX_TIME_DIFFERENCE_HOURS = 6.0


def calculate_scores(df):
    """
    Calculate an attribution evidence score for each AIS record.

    The score combines:
    - spatial proximity
    - temporal proximity
    - vessel movement information

    Returns
    -------
    pandas.DataFrame
        DataFrame with individual evidence scores and
        a combined attribution score.
    """

    df = df.copy()

    # Closer vessels receive stronger spatial evidence.
    df["spatial_score"] = (
        1 - df["distance_km"] / MAX_DISTANCE_KM
    ).clip(0, 1)

    # Vessels observed closer to the suspected spill time
    # receive stronger temporal evidence.
    df["temporal_score"] = (
        1 - df["time_difference_hours"] / MAX_TIME_DIFFERENCE_HOURS
    ).clip(0, 1)

    # For the MVP, combine spatial and temporal evidence.
    # These weights can be refined after validation.
    df["attribution_score"] = (
        0.60 * df["spatial_score"]
        + 0.40 * df["temporal_score"]
    )

    # Highest-scoring AIS observations should appear first.
    df = df.sort_values(
        "attribution_score",
        ascending=False,
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":
    print("AIS scoring module ready.")