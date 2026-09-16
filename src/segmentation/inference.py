import torch
import numpy as np
from PIL import Image
import rasterio
from rasterio.windows import Window

from src.segmentation.model import UNet
from src.segmentation.setup import get_device


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


def detect_oil_tiled(image_path, tile_size=256):
    model, device = load_model()
    
    with rasterio.open(image_path) as src:
        oil_mask_full = np.zeros((src.height, src.width), dtype=bool)
        
        for row in range(0, src.height, tile_size):
            for col in range(0, src.width, tile_size):
                window = Window(col, row, tile_size, tile_size)
                tile = src.read(1, window=window)
                
                actual_h, actual_w = tile.shape
                pad_r = tile_size - actual_h
                pad_c = tile_size - actual_w
                tile_padded = np.pad(tile, ((0, pad_r), (0, pad_c)), mode='constant')
                
                image_array = np.array(tile_padded, dtype=np.float32) / 255.0
                image_tensor = torch.from_numpy(image_array).unsqueeze(0).unsqueeze(0).to(device)
                
                with torch.no_grad():
                    prediction = model(image_tensor)
                
                tile_mask = (torch.sigmoid(prediction[0, 0]) > 0.5).cpu().numpy()
                oil_mask_full[row:row+actual_h, col:col+actual_w] = tile_mask[:actual_h, :actual_w]
                
    return oil_mask_full



if __name__ == "__main__":
    print("Inference module loaded successfully.")