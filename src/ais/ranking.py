"""
OASIS - AIS Vessel Ranking

M4: Vessel Attribution

Ranks candidate vessels using their attribution scores.
"""

import pandas as pd


def rank_vessels(df, top_n=10):
    """
    Return the highest-scoring unique vessels for a suspected oil spill.

    Parameters:
        df: DataFrame containing scored AIS observations.
        top_n: Number of top vessel candidates to return.

    Returns:
        DataFrame containing the top unique vessel candidates.
    """

    # Sort AIS observations from strongest attribution evidence to weakest.
    ranked = df.sort_values(
        "attribution_score",
        ascending=False
    ).reset_index(drop=True)

    # Keep only the strongest observation for each unique vessel.
    # This prevents one vessel with many AIS observations from
    # appearing repeatedly in the final candidate list.
    ranked = ranked.drop_duplicates(
        subset="MMSI",
        keep="first",
    )

    # Return the requested number of unique vessel candidates.
    return ranked.head(top_n)


if __name__ == "__main__":
    print("AIS ranking module ready.")