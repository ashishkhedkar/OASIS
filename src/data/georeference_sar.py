"""
OASIS - SAR Geolocation Grid

M1: Data Preparation
Creates a geolocation grid from Sentinel-1 annotation metadata.
"""

from pathlib import Path
import csv

from sar_geolocation import extract_geolocation_points


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_SAR_DIR = PROJECT_ROOT / "data" / "raw" / "sar"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"

OUTPUT_FILE = METADATA_DIR / "sar_geolocation_grid.csv"


def save_geolocation_grid(xml_file, output_file):
    """Extract and save Sentinel-1 geolocation grid points."""

    points = extract_geolocation_points(xml_file)

    if not points:
        raise ValueError("No geolocation points found.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["line", "pixel", "latitude", "longitude"]
        )

        writer.writeheader()
        writer.writerows(points)

    print(f"Saved {len(points)} geolocation points.")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    xml_files = list(RAW_SAR_DIR.glob("*vv*.xml"))

    if not xml_files:
        print("No VV annotation XML file found.")
    else:
        save_geolocation_grid(xml_files[0], OUTPUT_FILE)