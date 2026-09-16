"""
OASIS - Data Preprocessing Module

M1: Data Collection
Provides basic file validation and preparation
before data is used by the processing pipeline.
"""

from pathlib import Path


SUPPORTED_EXTENSIONS = {
    "sar": [".tif", ".tiff", ".zip"],
    "ais": [".csv", ".parquet", ".json"],
    "ocean": [".nc", ".nc4", ".zarr"],
    "wind": [".nc", ".nc4", ".zarr"],
}


def validate_file(file_path, data_type):
    """
    Check whether a file has a supported extension.
    """

    file_path = Path(file_path)

    if data_type not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Invalid data type. Use: sar, ais, ocean, or wind."
        )

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS[data_type]:
        print(
            f"Warning: {file_path.name} may not be a supported "
            f"{data_type} file."
        )
        return False

    print(f"Valid {data_type} file: {file_path.name}")
    return True


if __name__ == "__main__":
    print("Data preprocessing module is ready.")