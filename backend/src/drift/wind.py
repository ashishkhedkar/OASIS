from pathlib import Path

import xarray as xr


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WIND_DIR = PROJECT_ROOT / "data" / "raw" / "wind"


def get_wind(latitude, longitude, timestamp):
    """
    Return wind velocity at a given location and time
    using ERA5 data.

    Returns:
        Dictionary containing east and north
        wind components in m/s.
    """

    files = list(WIND_DIR.glob("*.nc"))

    if not files:
        raise FileNotFoundError(
            "No ERA5 wind NetCDF file found."
        )

    input_file = files[0]

    with xr.open_dataset(input_file) as dataset:

        selected = dataset.sel(
            latitude=latitude,
            longitude=longitude,
            valid_time=timestamp,
            method="nearest",
        )

        east_velocity = float(
            selected["u10"].values.squeeze()
        )

        north_velocity = float(
            selected["v10"].values.squeeze()
        )

    return {
        "east_mps": east_velocity,
        "north_mps": north_velocity,
    }


if __name__ == "__main__":
    wind = get_wind(
        latitude=13.2282,
        longitude=80.3633,
        timestamp="2017-01-29T12:00:00",
    )

    print("Wind data:")
    print(wind)