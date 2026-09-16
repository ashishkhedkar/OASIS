from src.drift.trajectory import generate_backtrack_trajectory
from src.drift.confidence import calculate_confidence
from src.drift.coordinate_utils import haversine_distance

import json
from pathlib import Path


def predict_origins(
    latitude,
    longitude,
    timestamp,
    total_hours=6,
    step_hours=1,
):
    """
    Estimate candidate spill origins using
    multiple drift hypotheses.
    """

    windage_variations = [
        0.02,
        0.025,
        0.03,
        0.035,
        0.04,
    ]

    all_origins = []

    for windage in windage_variations:

        trajectory = generate_backtrack_trajectory(
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp,
            total_hours=total_hours,
            step_hours=step_hours,
            windage_coefficient=windage,
        )

        for point in trajectory[1:]:

            confidence = calculate_confidence(
                point["hours_back"],
                max_backtrack_hours=total_hours,
            )

            all_origins.append(
                {
                    "latitude": point["latitude"],
                    "longitude": point["longitude"],
                    "hours_back": point["hours_back"],
                    "confidence": confidence,
                    "windage": windage,
                }
            )

    return all_origins


def group_origin_clusters(origins):
    """
    Group candidate origins by backtracking time.
    """

    clusters = {}

    for origin in origins:

        hours_back = origin["hours_back"]

        if hours_back not in clusters:
            clusters[hours_back] = []

        clusters[hours_back].append(origin)

    return clusters


def calculate_cluster_centers(clusters):
    """
    Calculate the average latitude, longitude,
    confidence, and uncertainty distance
    for each origin cluster.
    """

    centers = []

    for hours_back, points in clusters.items():

        total_latitude = sum(
            point["latitude"]
            for point in points
        )

        total_longitude = sum(
            point["longitude"]
            for point in points
        )

        total_confidence = sum(
            point["confidence"]
            for point in points
        )

        center_latitude = (
            total_latitude / len(points)
        )

        center_longitude = (
            total_longitude / len(points)
        )

        average_confidence = (
            total_confidence / len(points)
        )

        max_distance = max(
            haversine_distance(
                center_latitude,
                center_longitude,
                point["latitude"],
                point["longitude"],
            )
            for point in points
        )

        centers.append(
            {
                "hours_back": hours_back,
                "latitude": center_latitude,
                "longitude": center_longitude,
                "points": len(points),
                "confidence": average_confidence,
                "uncertainty_km": max_distance,
            }
        )

    # Sort by confidence from highest to lowest.
    centers.sort(
        key=lambda center: center["confidence"],
        reverse=True,
    )

    # Keep only the 5 most confident origin centers.
    centers = centers[:5]

    # Sort again by backtracking time.
    centers.sort(
        key=lambda center: center["hours_back"]
    )

    return centers


def save_probable_origins(centers):
    """
    Save the final probable origin centers
    for use by other project modules.
    """

    output_file = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "metadata"
        / "probable_origins.json"
    )

    with open(output_file, "w") as file:

        json.dump(
            centers,
            file,
            indent=4,
        )

    print(
        f"\nProbable origins saved to: "
        f"{output_file}"
    )


if __name__ == "__main__":

    origins = predict_origins(
        latitude=13.2282,
        longitude=80.3633,
        timestamp="2017-01-29T12:00:00",
        total_hours=6,
        step_hours=1,
    )

    clusters = group_origin_clusters(origins)

    centers = calculate_cluster_centers(clusters)

    print("\nProbable origin cluster centers:")

    for center in centers:

        print(
            f"{center['hours_back']}h back → "
            f"{center['latitude']:.6f}, "
            f"{center['longitude']:.6f} "
            f"({center['points']} hypotheses, "
            f"confidence: {center['confidence']:.2f}, "
            f"uncertainty: {center['uncertainty_km']:.2f} km)"
        )

    save_probable_origins(centers)