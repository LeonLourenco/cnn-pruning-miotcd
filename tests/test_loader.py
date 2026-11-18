"""Carregamento e pre-processamento das imagens."""
import os

import torch

from src.data import MIOTCDDataset, get_transforms
from src.utils import load_config


def _ds(root, smoke_dir, split, train=False):
    cfg = load_config(os.path.join(root, "configs", "smoke.yaml"))
    return MIOTCDDataset(os.path.join(smoke_dir, "split_smoke.csv"), os.path.join(smoke_dir, "img"),
                         split, cfg["data"]["classes"], get_transforms(train, 112)), cfg


def test_tamanho_por_split(root, smoke_dir):
    for split in ("train", "val", "test"):
        ds, _ = _ds(root, smoke_dir, split)
        assert len(ds) == 11 * 12


def test_formato_e_rotulos(root, smoke_dir):
    ds, cfg = _ds(root, smoke_dir, "test")
    labels = set()
    for i in range(len(ds)):
        x, y = ds[i]
        assert x.shape == (3, 112, 112) and x.dtype == torch.float32
        assert torch.isfinite(x).all()
        labels.add(y)
    assert labels == set(range(11))
    # rotulo do dataset corresponde a classe do CSV
    img_id, cls = ds.items[0]
    assert cfg["data"]["classes"][ds[0][1]] == cls


def test_avaliacao_deterministica(root, smoke_dir):
    ds, _ = _ds(root, smoke_dir, "test")
    assert torch.equal(ds[5][0], ds[5][0])
