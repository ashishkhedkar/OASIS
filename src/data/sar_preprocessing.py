"""
OASIS - SAR Preprocessing

M1: Data Preparation
Creates normalized SAR images for further analysis.
"""

from pathlib import Path

import numpy as np
import rasterio


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_SAR_DIR = PROJECT_ROOT / "data" / "raw" / "sar"
PROCESSED_SAR_DIR = PROJECT_ROOT / "data" / "processed" / "sar"


def normalize_sar(input_file, output_file):
    """
    Normalize a SAR image using percentile-based contrast stretching.
    """

    with rasterio.open(input_file) as src:
        data = src.read(1).astype(np.float32)
        profile = src.profile.copy()

    valid_data = data[data > 0]

    low = np.percentile(valid_data, 2)
    high = np.percentile(valid_data, 98)

    normalized = np.clip(
        (data - low) / (high - low),
        0,
        1
    )

    profile.update(
        dtype="float32",
        count=1,
        compress="lzw"
    )

    with rasterio.open(output_file, "w", **profile) as dst:
        dst.write(normalized.astype(np.float32), 1)


if __name__ == "__main__":
    PROCESSED_SAR_DIR.mkdir(parents=True, exist_ok=True)

    for file in RAW_SAR_DIR.glob("*.tiff"):
        output_file = PROCESSED_SAR_DIR / f"{file.stem}_normalized.tiff"

        print(f"Processing: {file.name}")

        normalize_sar(file, output_file)

        print(f"Saved: {output_file.name}")

    print("SAR preprocessing completed.")