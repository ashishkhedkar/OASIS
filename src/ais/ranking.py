"""
OASIS - AIS Vessel Ranking

M4: Vessel Attribution
Ranks candidate vessels using their attribution scores.
"""


def rank_vessels(df, top_n=10):
    """
    Return the highest-scoring vessels for a suspected oil spill.

    Parameters:
        df: DataFrame containing scored AIS observations.
        top_n: Number of top vessel observations to return.
    """

    # Sort vessels from strongest attribution evidence to weakest.
    ranked = df.sort_values(
        "attribution_score",
        ascending=False
    ).reset_index(drop=True)

    # Keep only the requested number of top candidates.
    return ranked.head(top_n)


if __name__ == "__main__":
    print("AIS ranking module ready.")