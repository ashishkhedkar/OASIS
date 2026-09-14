import torch

from src.dataloader import create_dataloaders
from src.metrics import dice_score, iou_score
from src.model import UNet
from src.setup import get_device


MODEL_PATH = "models/best_unet.pth"
BATCH_SIZE = 8


def evaluate():
    device = get_device()

    print("Using device:", device)

    _, val_loader = create_dataloaders(batch_size=BATCH_SIZE)

    model = UNet().to(device)

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device,
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    total_dice = 0.0
    total_iou = 0.0
    num_batches = 0

    with torch.no_grad():
        for images, masks in val_loader:
            images = images.to(device)
            masks = masks.to(device)

            predictions = model(images)

            total_dice += dice_score(predictions, masks)
            total_iou += iou_score(predictions, masks)

            num_batches += 1

    average_dice = total_dice / num_batches
    average_iou = total_iou / num_batches

    print()
    print("Evaluation complete.")
    print(f"Validation Dice: {average_dice:.4f}")
    print(f"Validation IoU: {average_iou:.4f}")


if __name__ == "__main__":
    evaluate()