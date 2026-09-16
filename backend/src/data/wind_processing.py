"""
OASIS - Wind Data Processing

M1: Data Preparation
Inspects and summarizes ERA5 wind data.
"""

from pathlib import Path

import xarray as xr


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WIND_DIR = PROJECT_ROOT / "data" / "raw" / "wind"


def inspect_wind_data():
    """Inspect the collected ERA5 wind NetCDF file."""

    files = list(WIND_DIR.glob("*.nc"))

    if not files:
        print("No NetCDF wind file found.")
        return

    input_file = files[0]

    print(f"Opening: {input_file.name}")

    with xr.open_dataset(input_file) as dataset:

        print("Variables:", list(dataset.data_vars))
        print("Dimensions:", dict(dataset.sizes))

        if "u10" in dataset:
            print("10m eastward wind (u10) available.")

        if "v10" in dataset:
            print("10m northward wind (v10) available.")

        print("Wind-data inspection completed.")


if __name__ == "__main__":
    inspect_wind_data()