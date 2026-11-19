"""Utilitarios compartilhados: configuracao, sementes, dispositivo e JSON."""
import json
import os
import random
import sys

import numpy as np
import torch
import yaml


def utf8_stdout():
    """Forca UTF-8 na saida do terminal. No Windows o padrao (cp1252) nao tem
    caracteres como '−' e 'Δ' e o print quebra com UnicodeEncodeError."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def load_config(path="configs/default.yaml"):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def set_seed(seed: int):
    """Fixa todas as fontes de aleatoriedade para reprodutibilidade."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def save_json(obj, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)


def exp_name(exp_id: int, tag: str, seed: int) -> str:
    """Padrao de nomes de arquivos: exp1_baseline_s0, exp3_l1_60_s0, ..."""
    return f"exp{exp_id}_{tag}_s{seed}"
