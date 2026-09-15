"""
OASIS - Data Loader

M1: Data Collection
Provides simple utilities to locate collected datasets.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"


def get_data_directory(data_type, processed=False):
    """
    Return the directory for a particular data source.

    data_type: sar, ais, ocean, or wind
    processed: True for processed data, False for raw data
    """

    valid_types = {"sar", "ais", "ocean", "wind"}

    if data_type not in valid_types:
        raise ValueError(
            "Invalid data type. Use: sar, ais, ocean, or wind."
        )

    folder = "processed" if processed else "raw"

    return DATA_ROOT / folder / data_type


def list_data_files(data_type, processed=False):
    """List files available for a selected data source."""

    directory = get_data_directory(data_type, processed)

    if not directory.exists():
        return []

    return [
        file for file in directory.iterdir()
        if file.is_file()
    ]


if __name__ == "__main__":
    print("Data loader module is ready.")

    for data_type in ["sar", "ais", "ocean", "wind"]:
        directory = get_data_directory(data_type)
        print(f"{data_type.upper()}: {directory}")