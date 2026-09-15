"""
OASIS - Ocean Current Processing

M1: Data Preparation
Inspects and summarizes ocean-current data
collected from Copernicus Marine.
"""

from pathlib import Path

import xarray as xr


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OCEAN_DIR = PROJECT_ROOT / "data" / "raw" / "ocean"


def inspect_ocean_data():
    """Inspect the collected ocean-current NetCDF file."""

    files = list(OCEAN_DIR.glob("*.nc"))

    if not files:
        print("No NetCDF file found.")
        return

    input_file = files[0]

    print(f"Opening: {input_file.name}")

    with xr.open_dataset(input_file) as dataset:

        print("Variables:", list(dataset.data_vars))
        print("Dimensions:", dict(dataset.sizes))

        if "uo" in dataset:
            print("Eastward current (uo) available.")

        if "vo" in dataset:
            print("Northward current (vo) available.")

        print("Ocean-current data inspection completed.")


if __name__ == "__main__":
    inspect_ocean_data()