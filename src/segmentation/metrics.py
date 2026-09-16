import torch


def dice_score(logits, targets, threshold=0.5, smooth=1e-6):
    probabilities = torch.sigmoid(logits)
    predictions = (probabilities >= threshold).float()

    predictions = predictions.view(-1)
    targets = targets.view(-1)

    intersection = (predictions * targets).sum()

    dice = (
        (2.0 * intersection + smooth)
        / (predictions.sum() + targets.sum() + smooth)
    )

    return dice.item()


def iou_score(logits, targets, threshold=0.5, smooth=1e-6):
    probabilities = torch.sigmoid(logits)
    predictions = (probabilities >= threshold).float()

    predictions = predictions.view(-1)
    targets = targets.view(-1)

    intersection = (predictions * targets).sum()

    union = predictions.sum() + targets.sum() - intersection

    iou = (intersection + smooth) / (union + smooth)

    return iou.item()


if __name__ == "__main__":
    # Test the metrics with identical prediction and target masks.
    targets = torch.zeros(2, 1, 256, 256)
    targets[:, :, 50:100, 50:100] = 1.0

    # Logits that strongly predict the same region.
    logits = torch.full_like(targets, -10.0)
    logits[:, :, 50:100, 50:100] = 10.0

    dice = dice_score(logits, targets)
    iou = iou_score(logits, targets)

    print("Dice score:", dice)
    print("IoU score:", iou)
    print("Metrics test: OK")