import torch
from torch.utils.data import DataLoader

from src.segmentation.dataset import OilSpillDataset


TRAIN_IMAGES = "Deep-SAR-Oil-Spill-Segmentation-Refined/images/images/train"
TRAIN_MASKS = "Deep-SAR-Oil-Spill-Segmentation-Refined/masks/masks/train"

VAL_IMAGES = "Deep-SAR-Oil-Spill-Segmentation-Refined/images/images/val"
VAL_MASKS = "Deep-SAR-Oil-Spill-Segmentation-Refined/masks/masks/val"


def create_dataloaders(batch_size=8):
    train_dataset = OilSpillDataset(
        images_dir=TRAIN_IMAGES,
        masks_dir=TRAIN_MASKS,
    )

    val_dataset = OilSpillDataset(
        images_dir=VAL_IMAGES,
        masks_dir=VAL_MASKS,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )

    return train_loader, val_loader


if __name__ == "__main__":
    train_loader, val_loader = create_dataloaders()

    images, masks = next(iter(train_loader))

    print("Train batches:", len(train_loader))
    print("Validation batches:", len(val_loader))

    print("Image batch shape:", images.shape)
    print("Mask batch shape:", masks.shape)

    print("Image dtype:", images.dtype)
    print("Mask dtype:", masks.dtype)

    print("Image range:", images.min().item(), images.max().item())
    print("Mask values:", torch.unique(masks).tolist())