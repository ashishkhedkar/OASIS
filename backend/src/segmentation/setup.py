import torch

from src.segmentation.model import UNet
from src.segmentation.losses import BCEDiceLoss


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def create_training_components():
    device = get_device()

    model = UNet().to(device)
    loss_fn = BCEDiceLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    return model, loss_fn, optimizer, device


if __name__ == "__main__":
    model, loss_fn, optimizer, device = create_training_components()

    print("Device:", device)
    print("Model device:", next(model.parameters()).device)

    # Small test batch.
    images = torch.randn(2, 1, 256, 256).to(device)
    masks = torch.randint(0, 2, (2, 1, 256, 256)).float().to(device)

    optimizer.zero_grad()

    predictions = model(images)
    loss = loss_fn(predictions, masks)

    loss.backward()
    optimizer.step()

    print("Input device:", images.device)
    print("Output device:", predictions.device)
    print("Loss:", loss.item())
    print("Optimizer step: OK")