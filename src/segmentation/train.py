import torch
from tqdm import tqdm

from src.segmentation.dataloader import create_dataloaders
from src.segmentation.losses import BCEDiceLoss
from src.segmentation.metrics import dice_score, iou_score
from src.segmentation.model import UNet
from src.segmentation.setup import get_device


EPOCHS = 5
BATCH_SIZE = 8
LEARNING_RATE = 1e-4

BEST_MODEL_PATH = "models/best_unet.pth"


def train_one_epoch(
    model,
    loader,
    loss_fn,
    optimizer,
    device,
):
    model.train()

    total_loss = 0.0

    progress = tqdm(loader, desc="Training")

    for images, masks in progress:

        images = images.to(device)
        masks = masks.to(device)

        optimizer.zero_grad()

        predictions = model(images)

        loss = loss_fn(predictions, masks)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

        progress.set_postfix(loss=f"{loss.item():.4f}")

    return total_loss / len(loader)


def validate(
    model,
    loader,
    loss_fn,
    device,
):
    model.eval()

    total_loss = 0.0
    total_dice = 0.0
    total_iou = 0.0

    with torch.no_grad():

        progress = tqdm(loader, desc="Validation")

        for images, masks in progress:

            images = images.to(device)
            masks = masks.to(device)

            predictions = model(images)

            loss = loss_fn(predictions, masks)
            dice = dice_score(predictions, masks)
            iou = iou_score(predictions, masks)

            total_loss += loss.item()
            total_dice += dice
            total_iou += iou

            progress.set_postfix(
                loss=f"{loss.item():.4f}",
                dice=f"{dice:.4f}",
                iou=f"{iou:.4f}",
            )

    return (
        total_loss / len(loader),
        total_dice / len(loader),
        total_iou / len(loader),
    )


if __name__ == "__main__":
    device = get_device()

    print("Using device:", device)

    train_loader, val_loader = create_dataloaders(
        batch_size=BATCH_SIZE
    )

    model = UNet().to(device)

    loss_fn = BCEDiceLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    best_dice = 0.0

    print()
    print("Starting training...")
    print(f"Epochs: {EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Learning rate: {LEARNING_RATE}")
    print()

    for epoch in range(EPOCHS):

        print(f"========== Epoch {epoch + 1}/{EPOCHS} ==========")

        train_loss = train_one_epoch(
            model=model,
            loader=train_loader,
            loss_fn=loss_fn,
            optimizer=optimizer,
            device=device,
        )

        print(f"Training loss: {train_loss:.4f}")

        val_loss, val_dice, val_iou = validate(
            model=model,
            loader=val_loader,
            loss_fn=loss_fn,
            device=device,
        )

        print(f"Validation loss: {val_loss:.4f}")
        print(f"Validation Dice: {val_dice:.4f}")
        print(f"Validation IoU: {val_iou:.4f}")

        # Save the model whenever validation Dice improves.
        if val_dice > best_dice:

            best_dice = val_dice

            checkpoint = {
                "epoch": epoch + 1,
                "model_state_dict": {
                    key: value.detach().cpu()
                    for key, value in model.state_dict().items()
                },
                "optimizer_state_dict": optimizer.state_dict(),
                "val_dice": val_dice,
                "val_iou": val_iou,
            }

            torch.save(checkpoint, BEST_MODEL_PATH)

            print(f"New best model saved: {BEST_MODEL_PATH}")

        print()

    print("Training complete.")
    print(f"Best validation Dice: {best_dice:.4f}")
    print(f"Best model: {BEST_MODEL_PATH}")