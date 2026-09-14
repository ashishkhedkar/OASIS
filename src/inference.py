import torch
import numpy as np
from PIL import Image

from src.model import UNet
from src.setup import get_device


MODEL_PATH = "models/best_unet.pth"


def load_model():
    device = get_device()

    model = UNet().to(device)

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device,
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, device


def detect_oil(image_path):
    model, device = load_model()

    # Load SAR image as grayscale
    image = Image.open(image_path).convert("L")

    # Convert to NumPy and normalize
    image_array = np.array(image, dtype=np.float32) / 255.0

    # Convert to PyTorch tensor
    image_tensor = torch.from_numpy(image_array).unsqueeze(0).unsqueeze(0)

    image_tensor = image_tensor.to(device)

    # Run model
    with torch.no_grad():
        prediction = model(image_tensor)

    # Convert model output to binary oil mask
    oil_mask = (
        torch.sigmoid(prediction[0, 0]) > 0.5
    ).cpu().numpy()

    return oil_mask


if __name__ == "__main__":
    print("Inference module loaded successfully.")