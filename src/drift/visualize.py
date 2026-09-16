import folium

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
    """Create a map showing drift hypotheses and probable origins."""

    # Create map centered around the observed spill.
    map_view = folium.Map(
        location=[
            spill_latitude,
            spill_longitude,
        ],
        zoom_start=11,
        tiles="Esri.WorldStreetMap",
    )

    # Mark observed spill location.
    folium.Marker(
        [
            spill_latitude,
            spill_longitude,
        ],
        popup="Observed Spill",
        tooltip="Observed Spill",
        icon=folium.Icon(
            color="red",
            icon="info-sign",
        ),
    ).add_to(map_view)

    # Plot each windage trajectory.
    windages = sorted(
        set(origin["windage"] for origin in origins)
    )

    for windage in windages:

        points = [
            origin
            for origin in origins
            if origin["windage"] == windage
        ]

        coordinates = [
            [
                point["latitude"],
                point["longitude"],
            ]
            for point in points
        ]

        folium.PolyLine(
            coordinates,
            tooltip=f"Windage {windage:.3f}",
        ).add_to(map_view)

    # Plot probable origin centers and uncertainty circles.
    for center in centers:

        latitude = center["latitude"]
        longitude = center["longitude"]

        folium.Marker(
            [
                latitude,
                longitude,
            ],
            popup=(
                f"Origin: {center['hours_back']}h back<br>"
                f"Confidence: {center['confidence']:.2f}<br>"
                f"Uncertainty: "
                f"{center['uncertainty_km']:.2f} km"
            ),
            tooltip=(
                f"Probable Origin - "
                f"{center['hours_back']}h back"
            ),
        ).add_to(map_view)

        folium.Circle(
            [
                latitude,
                longitude,
            ],
            radius=center["uncertainty_km"] * 1000,
            fill=False,
            tooltip=(
                f"Uncertainty: "
                f"{center['uncertainty_km']:.2f} km"
            ),
        ).add_to(map_view)

    # Save the interactive map.
    output_file = "probable_origin_map.html"

    map_view.save(output_file)

    print(
        f"\nInteractive map saved to: "
        f"{output_file}"
    )


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