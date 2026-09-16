"""
OASIS - AIS Loader

M4: Vessel Attribution
Loads the AIS dataset produced for vessel tracking and attribution.
"""

from pathlib import Path
import pandas as pd


# Project root: OASIS/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Location of the local M4 AIS dataset.
AIS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "ais"
    / "m4_ais_dataset"
    / "processed_AIS_dataset.csv"
)

# These are the minimum fields M4 needs for spatial and temporal analysis.
REQUIRED_COLUMNS = [
    "MMSI",
    "BaseDateTime",
    "LAT",
    "LON",
    "SOG",
    "COG",
    "Heading",
]


def load_ais_data(file_path=AIS_FILE):
    """Load the AIS CSV file and verify that required fields exist."""

    if not Path(file_path).exists():
        raise FileNotFoundError(
            f"AIS dataset not found at: {file_path}"
        )

    df = pd.read_csv(file_path)

    # Check the schema before passing data to the next M4 module.
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"AIS dataset is missing required columns: {missing_columns}"
        )

    return df


if __name__ == "__main__":
    ais_data = load_ais_data()

    print("AIS dataset loaded successfully.")
    print(f"Records: {len(ais_data)}")
    print(f"Columns: {len(ais_data.columns)}")
    print("Required M4 fields:")
    
    for column in REQUIRED_COLUMNS:
        print(f"- {column}")