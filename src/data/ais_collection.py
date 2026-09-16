"""
OASIS - AIS Data Collection

M1: Data Collection
Collects historical AIS vessel presence data
for the Ennore oil spill study area.
"""

from pathlib import Path
import os
import json
import requests

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AIS_DIR = PROJECT_ROOT / "data" / "raw" / "ais"

API_URL = "https://gateway.api.globalfishingwatch.org/v3/4wings/report"


def collect_ais_data():
    """Collect AIS vessel presence data for the Ennore study area."""

    load_dotenv()

    token = os.getenv("GFW_API_TOKEN")

    if not token:
        raise ValueError("GFW_API_TOKEN not found in .env")

    params = {
        "spatial-resolution": "LOW",
        "temporal-resolution": "DAILY",
        "group-by": "MMSI",
        "datasets[0]": "public-global-presence:latest",
        "date-range": "2017-01-28,2017-01-30",
        "format": "JSON",
        "spatial-aggregation": "true"
    }

    body = {
        "geojson": {
            "type": "Polygon",
            "coordinates": [[
                [80.30, 13.18],
                [80.42, 13.18],
                [80.42, 13.28],
                [80.30, 13.28],
                [80.30, 13.18]
            ]]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        API_URL,
        params=params,
        json=body,
        headers=headers
    )

    response.raise_for_status()

    AIS_DIR.mkdir(parents=True, exist_ok=True)

    output_file = AIS_DIR / "ennore_ais_2017.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=2)

    print("AIS data collected successfully.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    collect_ais_data()