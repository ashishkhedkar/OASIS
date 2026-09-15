"""
OASIS - AIS Processing

M1: Data Preparation
Converts collected AIS vessel-presence JSON
into a clean CSV file for further analysis.
"""

from pathlib import Path
import json
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AIS_DIR = PROJECT_ROOT / "data" / "raw" / "ais"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"

INPUT_FILE = AIS_DIR / "ennore_ais_2017.json"
OUTPUT_FILE = METADATA_DIR / "ennore_ais_2017.csv"


def process_ais_data():
    """Convert AIS JSON records into CSV format."""

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    records = []

    for entry in data.get("entries", []):
        for dataset_name, vessels in entry.items():

            for vessel in vessels:
                records.append({
                    "date": vessel.get("date"),
                    "entryTimestamp": vessel.get("entryTimestamp"),
                    "exitTimestamp": vessel.get("exitTimestamp"),
                    "hours": vessel.get("hours"),
                    "mmsi": vessel.get("mmsi")
                })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "date",
            "entryTimestamp",
            "exitTimestamp",
            "hours",
            "mmsi"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print("AIS processing completed.")
    print(f"Records saved: {len(records)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    process_ais_data()