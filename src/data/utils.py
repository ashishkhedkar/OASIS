"""
OASIS - Data Utilities

M1: Data Collection
Common helper functions used by the data pipeline.
"""

from pathlib import Path


def get_file_size(file_path):
    """Return file size in megabytes."""

    file_path = Path(file_path)

    if not file_path.exists():
        return 0.0

    return file_path.stat().st_size / (1024 * 1024)


def ensure_directory(directory):
    """Create a directory if it does not already exist."""

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

    return directory


def get_file_extension(file_path):
    """Return the file extension in lowercase."""

    return Path(file_path).suffix.lower()


if __name__ == "__main__":
    print("Data utilities module is ready.")