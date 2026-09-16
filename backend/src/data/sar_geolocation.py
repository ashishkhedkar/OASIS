"""
OASIS - SAR Geolocation Utilities

M1: Data Preparation
Extracts geolocation grid points from Sentinel-1
annotation XML files.
"""

from pathlib import Path
import xml.etree.ElementTree as ET


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_SAR_DIR = PROJECT_ROOT / "data" / "raw" / "sar"


def extract_geolocation_points(xml_file):
    """
    Extract latitude and longitude from Sentinel-1
    geolocation grid points.
    """

    root = ET.parse(xml_file).getroot()

    points = []

    for point in root.iter():
        if not point.tag.endswith("geolocationGridPoint"):
            continue

        values = {}

        for child in point:
            name = child.tag.split("}")[-1]

            if name in ["line", "pixel", "latitude", "longitude"]:
                values[name] = float(child.text)

        if len(values) == 4:
            points.append(values)

    return points


if __name__ == "__main__":
    xml_files = list(RAW_SAR_DIR.glob("*vv*.xml"))

    if not xml_files:
        print("No VV annotation XML file found.")
    else:
        points = extract_geolocation_points(xml_files[0])

        print("Geolocation points extracted:", len(points))

        if points:
            print("First point:")
            print(points[0])