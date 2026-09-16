from datetime import datetime, timezone
from pathlib import Path

import xarray as xr


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OCEAN_DIR = PROJECT_ROOT / "data" / "raw" / "ocean"


def get_current(latitude, longitude, timestamp):
    """
    Return ocean current velocity at a given
    location and time using Copernicus Marine data.

    Spatial location uses the nearest available grid point.
    Time is linearly interpolated between available daily values.

    Returns:
        Dictionary containing east and north
        current components in m/s.
    """

    files = list(OCEAN_DIR.glob("*.nc"))

    if not files:
        raise FileNotFoundError(
            "No ocean-current NetCDF file found."
        )

    input_file = files[0]

    requested_time = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    if requested_time.tzinfo is not None:
        requested_time = requested_time.astimezone(
            timezone.utc
        ).replace(tzinfo=None)

    with xr.open_dataset(input_file) as dataset:

        selected = dataset.sel(
            latitude=latitude,
            longitude=longitude,
            method="nearest",
        )

        interpolated = selected.interp(
            time=requested_time,
        )

        east_velocity = float(
            interpolated["uo"].values.squeeze()
        )

        north_velocity = float(
            interpolated["vo"].values.squeeze()
        )

    return {
        "east_mps": east_velocity,
        "north_mps": north_velocity,
    }


if __name__ == "__main__":
    current = get_current(
        latitude=13.2282,
        longitude=80.3633,
        timestamp="2017-01-29T12:00:00",
    )

    print("Ocean current data:")
    print(current)