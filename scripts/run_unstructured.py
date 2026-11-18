"""Executa os Exp 2, 3 e 4 (poda L1 nao estruturada, 30/60/90%) para uma semente.

Fluxo igual ao run_structured.py:
  baseline da mesma semente -> seleciona pesos -> mascara e avalia ANTES do fine-tuning
  -> fine-tuning com mascara fixa -> salva modelo e metricas.

Uso:
    python scripts/run_unstructured.py --seed 0                 # 30, 60 e 90%
    python scripts/run_unstructured.py --seed 0 --amounts 0.3   # so uma intensidade
"""
import argparse
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import build_loaders  # noqa: E402
from src.evaluate import evaluate_model  # noqa: E402
from src.models import build_resnet18  # noqa: E402
from src.pruning.unstructured import apply_mask, mask_hook, select_weights, summarize_plan  # noqa: E402
from src.train import fit  # noqa: E402
from src.utils import exp_name, get_device, load_config, save_json, set_seed  # noqa: E402

# Intensidade (%) -> numero do experimento, conforme docs/SPEC.md
EXP_ID = {30: 2, 60: 3, 90: 4}


def run_one(cfg, a, amount, device):
    hp = dict(cfg["finetune"])
    if a.epochs:
        hp["epochs"] = a.epochs
    nc = len(cfg["data"]["classes"])
    pct = round(amount * 100)
    if pct not in EXP_ID:
        raise ValueError(f"intensidade {amount} fora do protocolo (use 0.3, 0.6 ou 0.9)")

    base = exp_name(1, "baseline", a.seed)
    name = exp_name(EXP_ID[pct], f"l1_{pct}", a.seed)
    out = os.path.join(a.results, name)
    os.makedirs(out, exist_ok=True)

    set_seed(a.seed)
    model = build_resnet18(nc, pretrained=False)
    model.load_state_dict(torch.load(os.path.join(a.results, base, f"{base}.pt"), map_location="cpu"))
    model.to(device)  # antes de selecionar: as mascaras ficam no mesmo device do modelo
    loaders = build_loaders(cfg, hp["batch_size"], seed=a.seed)

    # 1) selecao dos pesos + mascara, e avaliacao antes do fine-tuning
    plan = select_weights(model, amount, cfg)
    save_json({"exp": name, "seed": a.seed, "amount": amount, "scope": cfg["unstructured"]["scope"],
               **summarize_plan(plan)}, os.path.join(out, f"{name}_plan.json"))
    apply_mask(model, plan)
    pre = {"exp": name, "stage": "pre_finetune", **evaluate_model(model, cfg, loaders, device)}
    save_json(pre, os.path.join(out, f"{name}_prefinetune_metrics.json"))
    print(f"{name} antes do fine-tuning: f1_macro={pre['f1_macro']:.4f}")

    # 2) fine-tuning com mascara fixa
    model, history = fit(model, loaders, hp, device, after_step=mask_hook(plan),
                         max_batches=a.max_batches, log_prefix=f"[{name}] ")
    apply_mask(model, plan)  # garantia extra
    torch.save(model, os.path.join(out, f"{name}_model.pt"))
    save_json({"exp": name, "hp": hp, "history": history}, os.path.join(out, f"{name}_history.json"))
    res = {"exp": name, "stage": "final",
       **evaluate_model(model, cfg, loaders, device,
                        pred_path=os.path.join(out, f"{name}_predictions_test.csv"))}
    save_json(res, os.path.join(out, f"{name}_metrics.json"))
    print(f"{name}: f1_macro={res['f1_macro']:.4f} params_nonzero={res['params_nonzero']} "
          f"weight_sparsity={res['weight_sparsity']:.3f} size_gzip_mb={res['size_zip_mb']:.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--results", default="results")
    ap.add_argument("--amounts", type=float, nargs="+", default=None,
                    help="intensidades a rodar (padrao: unstructured.amounts do YAML)")
    ap.add_argument("--max-batches", type=int, default=None, help="so para smoke test")
    ap.add_argument("--epochs", type=int, default=None, help="sobrescreve (so para smoke test)")