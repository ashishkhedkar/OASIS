from pathlib import Path

import xarray as xr


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OCEAN_DIR = PROJECT_ROOT / "data" / "raw" / "ocean"


def get_current(latitude, longitude, timestamp):
    """
    Return ocean current velocity at a given
    location and time using Copernicus Marine data.

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

    with xr.open_dataset(input_file) as dataset:

        selected = dataset.sel(
            latitude=latitude,
            longitude=longitude,
            time=timestamp,
            method="nearest",
        )

        east_velocity = float(
            selected["uo"].values.squeeze()
        )

        north_velocity = float(
            selected["vo"].values.squeeze()
        )

    return {
        "east_mps": east_velocity,
        "north_mps": north_velocity,
    }


if __name__ == "__main__":
    current = get_current(
        latitude=13.2282,
        longitude=80.3633,
        timestamp="2017-01-29T00:00:00",
    )

    print("Ocean current data:")
    print(current)