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

    # Plot the estimated path from origin toward the observed spill.
    plt.plot(
        longitudes,
        latitudes,
        marker="o",
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Backtracked Oil Spill Trajectory")

    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    from src.drift.trajectory import (
        generate_backtrack_trajectory,
    )

    current = {
        "east_mps": 0.4,
        "north_mps": 0.1,
    }

    wind = {
        "east_mps": 2.0,
        "north_mps": 0.5,
    }

    trajectory = generate_backtrack_trajectory(
        latitude=18.52,
        longitude=72.85,
        current=current,
        wind=wind,
        total_hours=6,
        step_hours=1,
    )

    plot_trajectory(trajectory)