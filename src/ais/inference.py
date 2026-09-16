"""
OASIS - AIS Inference Pipeline

M4: Vessel Attribution

Connects all AIS processing modules into one pipeline:
loading -> preprocessing -> filtering -> feature extraction
-> scoring -> ranking.
"""

from src.ais.loader import load_ais_data
from src.ais.filtering import filter_nearby_vessels
from src.ais.features import calculate_attribution_features
from src.ais.scoring import calculate_scores
from src.ais.ranking import rank_vessels


def predict_vessels(
    origin_latitude,
    origin_longitude,
    origin_time,
    radius_km=10,
    top_n=10,
):
    """
    Identify and rank vessels that could be associated
    with a suspected oil-spill origin.

    Parameters:
        origin_latitude: Latitude of the candidate spill origin.
        origin_longitude: Longitude of the candidate spill origin.
        origin_time: Timestamp of the suspected spill.
        radius_km: Search radius around the origin.
        top_n: Number of highest-ranked vessels to return.
    """

    # Load the prepared AIS dataset.
    ais_data = load_ais_data()

    # Keep only vessels operating near the candidate origin.
    nearby_vessels = filter_nearby_vessels(
        ais_data,
        origin_latitude,
        origin_longitude,
        radius_km,
    )

    # Stop early if no AIS observations are within the search radius.
    if nearby_vessels.empty:
        return nearby_vessels

    # Calculate spatial and temporal evidence for each observation.
    features = calculate_attribution_features(
        nearby_vessels,
        origin_latitude,
        origin_longitude,
        origin_time,
    )

    # Combine the evidence into an attribution score.
    scored = calculate_scores(features)

    # Return the strongest vessel candidates first.
    ranked = rank_vessels(scored, top_n)

    return ranked

def predict_vessels_from_origins(origins, top_n=10):
    """
    Run M4 vessel attribution for multiple candidate origins
    produced by M3.
    """

    all_results = []

    for origin in origins:
        # Use M3's candidate origin as the center of the AIS search.
        results = predict_vessels(
            origin_latitude=origin["latitude"],
            origin_longitude=origin["longitude"],
            origin_time=None,
            radius_km=10,
            top_n=top_n,
        )

        if results.empty:
            continue

        # Attach M3 information so the final result keeps the
        # connection between a vessel and its candidate origin.
        results = results.copy()
        results["origin_latitude"] = origin["latitude"]
        results["origin_longitude"] = origin["longitude"]
        results["origin_hours_back"] = origin["hours_back"]
        results["origin_confidence"] = origin["confidence"]
        results["origin_uncertainty_km"] = origin["uncertainty_km"]

        all_results.append(results)

    if not all_results:
        return None

    return __import__("pandas").concat(all_results, ignore_index=True)
    
if __name__ == "__main__":
    # Example candidate origin used to test the complete M4 pipeline.
    results = predict_vessels(
        origin_latitude=25.77304,
        origin_longitude=-80.14296,
        origin_time="2022-03-31 00:01:29",
        radius_km=10,
        top_n=10,
    )

    print("\nM4 Vessel Attribution Results")
    print("=" * 60)

    if results.empty:
        print("No vessels found near the candidate origin.")
    else:
        print(
            results[
                [
                    "MMSI",
                    "LAT",
                    "LON",
                    "distance_km",
                    "time_difference_hours",
                    "spatial_score",
                    "temporal_score",
                    "attribution_score",
                ]
            ].to_string(index=False)
        )