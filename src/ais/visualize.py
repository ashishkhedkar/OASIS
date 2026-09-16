"""
OASIS - AIS Visualization

M4: Vessel Attribution
Visualizes candidate vessels around a suspected spill origin.
"""

import matplotlib.pyplot as plt


def plot_vessels(
    df,
    origin_latitude,
    origin_longitude,
    save_path=None,
):
    """
    Plot AIS vessel positions relative to a suspected spill origin.

    Parameters:
        df: DataFrame containing AIS observations.
        origin_latitude: Latitude of suspected spill origin.
        origin_longitude: Longitude of suspected spill origin.
        save_path: Optional path for saving the generated figure.
    """

    plt.figure(figsize=(10, 7))

    # Plot AIS observations using longitude as x and latitude as y.
    plt.scatter(
        df["LON"],
        df["LAT"],
        s=12,
        alpha=0.5,
        label="AIS vessels",
    )

    # Mark the suspected spill origin separately.
    plt.scatter(
        origin_longitude,
        origin_latitude,
        s=120,
        marker="*",
        label="Suspected spill origin",
    )

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("AIS Vessel Positions Around Suspected Spill Origin")
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    print("AIS visualization module ready.")