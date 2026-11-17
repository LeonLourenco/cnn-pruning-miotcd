"""Avaliacao padronizada de qualquer modelo (os 6 experimentos usam ESTE arquivo).

Gera um JSON com tres blocos (docs/SPEC.md, secao "Metricas"):
- preditivo: F1-macro (principal), acuracia, precisao/recall/F1 por classe, matriz de confusao;
- compressao: parametros totais e nao nulos, esparsidade dos pesos de conv/linear;
- custo: tamanho do state_dict em MB (puro e comprimido) e MACs medidos e teoricos.

MACs:
- `macs_measured`: conta pelo formato das camadas (o que o hardware realmente executa
  em tensores densos). Um modelo com pesos zerados tem os MESMOS MACs do original.
- `macs_theoretical`: MACs de cada camada multiplicados pela fracao de pesos nao nulos
  dela. E uma aproximacao do custo se os zeros fossem pulados.
A latencia NAO e medida aqui: ver scripts/benchmark_latency.py (somente no notebook do Leon).
"""
import argparse
import io
import os
import zlib

import torch
import torch.nn as nn
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support

from src.data import build_loaders
from src.train import predict
from src.utils import get_device, load_config, save_json


def _assert_no_prune_hooks(model):
    for n, _ in model.named_buffers():
        if n.endswith("_mask"):
            raise RuntimeError("modelo ainda tem mascaras do torch.nn.utils.prune: "
                               "chame prune.remove(...) antes de avaliar")


def count_params(model):
    total = sum(p.numel() for p in model.parameters())
    nonzero = sum(int((p != 0).sum()) for p in model.parameters())
    w = [m.weight for m in model.modules() if isinstance(m, (nn.Conv2d, nn.Linear))]
    w_total = sum(t.numel() for t in w)
    w_zero = sum(int((t == 0).sum()) for t in w)
    return {"params_total": total, "params_nonzero": nonzero,
            "weight_sparsity": w_zero / w_total}


def model_size_mb(model):
    buf = io.BytesIO()
    torch.save(model.state_dict(), buf)
    raw = buf.getvalue()
    return {"size_mb": len(raw) / 2**20,
            "size_zip_mb": len(zlib.compress(raw, 6)) / 2**20}


@torch.no_grad()
def count_macs(model, img_size=112):
    """Conta MACs de Conv2d e Linear com hooks (1 imagem)."""
    layers = []

    def hook(mod, inp, out):
        w = mod.weight
        if isinstance(mod, nn.Conv2d):
            per_out = (w.shape[1]) * w.shape[2] * w.shape[3]  # in/groups * kh * kw
            macs = out.numel() * per_out
        else:
            macs = w.shape[0] * w.shape[1]
        density = float((w != 0).sum()) / w.numel()
        layers.append((macs, density))

    hs = [m.register_forward_hook(hook) for m in model.modules()
          if isinstance(m, (nn.Conv2d, nn.Linear))]
    was_training = model.training
    model.eval()
    dev = next(model.parameters()).device
    model(torch.zeros(1, 3, img_size, img_size, device=dev))
    model.train(was_training)
    for h in hs:
        h.remove()
    return {"macs_measured": int(sum(m for m, _ in layers)),
            "macs_theoretical": int(sum(m * d for m, d in layers))}


def predictive_metrics(y, p, classes):
    pr, rc, f1, sup = precision_recall_fscore_support(
        y, p, labels=list(range(len(classes))), zero_division=0)
    return {
        "f1_macro": float(f1_score(y, p, average="macro")),
        "accuracy": float((y == p).mean()),
        "per_class": {c: {"precision": float(pr[i]), "recall": float(rc[i]),
                          "f1": float(f1[i]), "support": int(sup[i])}
                      for i, c in enumerate(classes)},
        "confusion_matrix": confusion_matrix(y, p, labels=list(range(len(classes)))).tolist(),
    }


def evaluate_model(model, cfg, loaders, device, split="test"):
    _assert_no_prune_hooks(model)
    model.to(device)
    y, p = predict(model, loaders[split], device)
    out = {"split": split, **predictive_metrics(y, p, cfg["data"]["classes"])}
    out.update(count_params(model))
    out.update(model_size_mb(model))
    out.update(count_macs(model, cfg["data"]["img_size"]))
    return out


def main():
    ap = argparse.ArgumentParser(description="Avalia um modelo salvo inteiro (torch.save(model))")
    ap.add_argument("--model", required=True, help="arquivo <exp>_model.pt")
    ap.add_argument("--exp", required=True, help="nome do experimento, ex.: exp5_struct_mask_50_s0")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--split", default="test", choices=["val", "test"])
    a = ap.parse_args()
    cfg = load_config(a.config)
    device = get_device()
    model = torch.load(a.model, map_location=device, weights_only=False)
    loaders = build_loaders(cfg, batch_size=256)
    res = {"exp": a.exp, **evaluate_model(model, cfg, loaders, device, a.split)}
    save_json(res, os.path.join(a.out_dir, a.exp, f"{a.exp}_metrics.json"))
    print(f"{a.exp}: f1_macro={res['f1_macro']:.4f} params_nonzero={res['params_nonzero']} "
          f"size_mb={res['size_mb']:.2f} macs={res['macs_measured']}")


if __name__ == "__main__":
    main()
