"""Carregamento do MIO-TCD a partir do split.csv.

Estrutura esperada das imagens: <img_root>/<classe>/<id>.jpg
(gerada por scripts/extract_subset.py; no Kaggle, o zip do dataset ja vem nesse formato).

Pre-processamento (docs/SPEC.md):
- redimensiona direto para img_size x img_size (sem corte central, para nao cortar o veiculo);
- treino: flip horizontal + RandomResizedCrop leve (escala 0.8-1.0);
- validacao/teste: sem aumento de dados;
- normalizacao do ImageNet.
"""
import csv
import os

import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def get_transforms(train: bool, size: int = 112):
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(size, scale=(0.8, 1.0), ratio=(0.75, 1.333)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    return transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])


class MIOTCDDataset(Dataset):
    def __init__(self, split_csv, img_root, split, classes, transform=None):
        self.img_root = img_root
        self.transform = transform
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        with open(split_csv, newline="") as fh:
            self.items = [(r["id"], r["classe"]) for r in csv.DictReader(fh) if r["split"] == split]
        if not self.items:
            raise ValueError(f"nenhuma imagem no split '{split}' de {split_csv}")

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        img_id, cls = self.items[i]
        img = Image.open(os.path.join(self.img_root, cls, f"{img_id}.jpg")).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.class_to_idx[cls]


def build_loaders(cfg, batch_size, seed=0):
    d = cfg["data"]
    g = torch.Generator()
    g.manual_seed(seed)
    loaders = {}
    for split in ("train", "val", "test"):
        ds = MIOTCDDataset(d["split_csv"], d["img_root"], split, d["classes"],
                           get_transforms(split == "train", d["img_size"]))
        loaders[split] = DataLoader(
            ds, batch_size=batch_size, shuffle=(split == "train"),
            num_workers=d["num_workers"], pin_memory=torch.cuda.is_available(),
            generator=g if split == "train" else None,
        )
    return loaders
