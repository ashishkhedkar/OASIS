# Total Loss = BCE Loss + Dice Loss

import torch
import torch.nn as nn


class DiceLoss(nn.Module):
    def __init__(self, smooth=1.0):
        super().__init__()
        self.smooth = smooth

    def forward(self, logits, targets):
        probabilities = torch.sigmoid(logits)

        probabilities = probabilities.view(-1)
        targets = targets.view(-1)

        intersection = (probabilities * targets).sum()

        dice = (
            (2.0 * intersection + self.smooth)
            / (
                probabilities.sum()
                + targets.sum()
                + self.smooth
            )
        )

        return 1.0 - dice


class BCEDiceLoss(nn.Module):
    def __init__(self):
        super().__init__()

        self.bce = nn.BCEWithLogitsLoss()
        self.dice = DiceLoss()

    def forward(self, logits, targets):
        bce_loss = self.bce(logits, targets)
        dice_loss = self.dice(logits, targets)

        return bce_loss + dice_loss