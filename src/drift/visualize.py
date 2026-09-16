import matplotlib.pyplot as plt

from src.drift.inference import (
    predict_origins,
    group_origin_clusters,
    calculate_cluster_centers,
)


def plot_origin_hypotheses(
    origins,
    centers,
    spill_latitude,
    spill_longitude,
):
    """Plot drift hypotheses and probable origin centers."""

    plt.figure(figsize=(9, 7))

    windages = sorted(
        set(origin["windage"] for origin in origins)
    )

    for windage in windages:

        points = [
            origin
            for origin in origins
            if origin["windage"] == windage
        ]

        latitudes = [
            point["latitude"]
            for point in points
        ]

        longitudes = [
            point["longitude"]
            for point in points
        ]

        plt.plot(
            longitudes,
            latitudes,
            marker="o",
            label=f"Windage {windage:.3f}",
        )

    # Plot probable origin cluster centers.
    center_latitudes = [
        center["latitude"]
        for center in centers
    ]

    center_longitudes = [
        center["longitude"]
        for center in centers
    ]

    plt.scatter(
        center_longitudes,
        center_latitudes,
        marker="*",
        s=180,
        label="Probable origin centers",
    )

    # Label each center with its confidence.
    for center in centers:

        plt.annotate(
            f"{center['hours_back']}h | "
            f"Confidence: {center['confidence']:.2f}",
            (
                center["longitude"],
                center["latitude"],
            ),
            xytext=(8, 8),
            textcoords="offset points",
        )

    # Mark observed spill location.
    plt.scatter(
        spill_longitude,
        spill_latitude,
        marker="x",
        s=120,
        label="Observed spill",
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Oil Spill Backtracking - Probable Origins")

    plt.grid(True)
    plt.legend()

    plt.show()


if __name__ == "__main__":

    spill_latitude = 13.2282
    spill_longitude = 80.3633

    origins = predict_origins(
        latitude=spill_latitude,
        longitude=spill_longitude,
        timestamp="2017-01-29T12:00:00",
        total_hours=6,
        step_hours=1,
    )

    clusters = group_origin_clusters(origins)

    centers = calculate_cluster_centers(clusters)

    plot_origin_hypotheses(
        origins,
        centers,
        spill_latitude,
        spill_longitude,
    )