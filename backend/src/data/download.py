"""
OASIS - Data Download Module

M1: Data Collection
Handles downloading and storing raw satellite, AIS,
ocean-current, and wind data.
"""

from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw data directories
RAW_DATA = PROJECT_ROOT / "data" / "raw"

SAR_DIR = RAW_DATA / "sar"
AIS_DIR = RAW_DATA / "ais"
OCEAN_DIR = RAW_DATA / "ocean"
WIND_DIR = RAW_DATA / "wind"


def create_data_directories():
    """Create raw data directories if they do not exist."""
    for directory in [SAR_DIR, AIS_DIR, OCEAN_DIR, WIND_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_data_directories()
    print("Raw data directories are ready.")