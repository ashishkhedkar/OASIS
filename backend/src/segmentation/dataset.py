from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset


class OilSpillDataset(Dataset):
    def __init__(self, images_dir, masks_dir):
        self.images_dir = Path(images_dir)
        self.masks_dir = Path(masks_dir)

        self.image_files = sorted(self.images_dir.glob("*.png"))

        if len(self.image_files) == 0:
            raise RuntimeError(f"No PNG images found in {self.images_dir}")

        # Make sure every image has a corresponding mask.
        for image_path in self.image_files:
            mask_path = self.masks_dir / image_path.name

            if not mask_path.exists():
                raise RuntimeError(
                    f"Missing mask for {image_path.name}: {mask_path}"
                )

        print(f"Found {len(self.image_files)} image/mask pairs.")

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, index):
        image_path = self.image_files[index]
        mask_path = self.masks_dir / image_path.name

        # Load as grayscale.
        image = Image.open(image_path).convert("L")
        mask = Image.open(mask_path).convert("L")

        # Convert PIL images to NumPy arrays.
        image = np.array(image, dtype=np.float32)
        mask = np.array(mask, dtype=np.float32)

        # Normalize SAR image from [0, 255] to [0, 1].
        image = image / 255.0

        # Convert mask to binary values: 0 = background, 1 = oil.
        mask = (mask > 0).astype(np.float32)

        # Convert to PyTorch tensors and add channel dimension.
        image = torch.from_numpy(image).unsqueeze(0)
        mask = torch.from_numpy(mask).unsqueeze(0)

        return image, mask