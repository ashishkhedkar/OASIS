import matplotlib.pyplot as plt
import torch

from src.segmentation.dataloader import create_dataloaders
from src.segmentation.model import UNet
from src.segmentation.setup import get_device


MODEL_PATH = "models/best_unet.pth"


def visualize():
    device = get_device()

    _, val_loader = create_dataloaders(batch_size=1)

    model = UNet().to(device)

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device,
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    iterator = iter(val_loader)

    for sample_number in range(5):
        images, masks = next(iterator)

        images = images.to(device)

        with torch.no_grad():
            predictions = model(images)

        image = images[0, 0].cpu().numpy()
        mask = masks[0, 0].numpy()

        prediction = (
            torch.sigmoid(predictions[0, 0]) > 0.5
        ).cpu().numpy()

        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        plt.imshow(image, cmap="gray")
        plt.title("SAR Image")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.imshow(mask, cmap="gray")
        plt.title("Actual Oil Spill")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.imshow(prediction, cmap="gray")
        plt.title("Predicted Oil Spill")
        plt.axis("off")

        plt.suptitle(f"Validation Sample {sample_number + 1}")
        plt.tight_layout()

        # Automatically move to the next sample
        plt.show(block=False)
        plt.pause(2)
        plt.close()


if __name__ == "__main__":
    visualize()