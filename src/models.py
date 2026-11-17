"""Construcao da ResNet-18 usada em todos os experimentos."""
import torch.nn as nn
from torchvision import models


def build_resnet18(num_classes: int, pretrained: bool = True) -> nn.Module:
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.resnet18(weights=weights)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
