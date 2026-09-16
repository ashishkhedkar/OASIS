import matplotlib.pyplot as plt


def plot_trajectory(trajectory):
    """Plot a backtracked spill trajectory."""

    latitudes = [
        point["latitude"]
        for point in trajectory
    ]

    longitudes = [
        point["longitude"]
        for point in trajectory
    ]

    plt.figure(figsize=(8, 6))

    # Plot the estimated backtracked path.
    plt.plot(
        longitudes,
        latitudes,
        marker="o",
    )

    # Mark the observed spill location.
    plt.scatter(
        longitudes[0],
        latitudes[0],
        marker="x",
        s=100,
        label="Observed spill",
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Backtracked Oil Spill Trajectory")

    plt.grid(True)
    plt.legend()

    # Label each point with hours back.
    for point in trajectory:
        plt.annotate(
            f"{point['hours_back']}h",
            (
                point["longitude"],
                point["latitude"],
            ),
        )

    plt.show()


if __name__ == "__main__":
    from src.drift.trajectory import (
        generate_backtrack_trajectory,
    )

    trajectory = generate_backtrack_trajectory(
        latitude=13.2282,
        longitude=80.3633,
        timestamp="2017-01-29T12:00:00",
        total_hours=6,
        step_hours=1,
    )

    plot_trajectory(trajectory)