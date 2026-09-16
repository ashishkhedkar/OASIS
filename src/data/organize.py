"""
OASIS - Data Organization Module

M1: Data Collection
Organizes raw data into the correct source folders.
"""

from pathlib import Path
import shutil


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"

DATA_DIRECTORIES = {
    "sar": RAW_DATA / "sar",
    "ais": RAW_DATA / "ais",
    "ocean": RAW_DATA / "ocean",
    "wind": RAW_DATA / "wind",
}


def organize_file(file_path, data_type):
    """
    Move a downloaded file into the appropriate raw-data folder.

    Parameters:
        file_path: Path of the downloaded file
        data_type: One of sar, ais, ocean, wind
    """

    if data_type not in DATA_DIRECTORIES:
        raise ValueError(
            "Invalid data type. Use: sar, ais, ocean, or wind."
        )

    source = Path(file_path)
    destination_folder = DATA_DIRECTORIES[data_type]

    destination_folder.mkdir(parents=True, exist_ok=True)

    destination = destination_folder / source.name
    shutil.move(str(source), str(destination))

    print(f"Moved {source.name} → data/raw/{data_type}/")


if __name__ == "__main__":
    print("Data organization module is ready.")