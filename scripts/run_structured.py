"""Executa os Exp 5 (estruturado com mascara) e Exp 6 (estruturado fisico) para uma semente.

Fluxo (docs/SPEC.md):
  baseline da mesma semente
    -> seleciona 50% dos canais por camada (L1)          [plano salvo em JSON]
    -> aplica mascara e avalia ANTES do fine-tuning      [exp5 ..._prefinetune_metrics.json]
    -> fine-tuning com a mascara fixa                    [exp5 final]
    -> remove fisicamente os mesmos canais               [exp6 final]
    -> confere que mascara e fisico dao a mesma saida

Uso:
    python scripts/run_structured.py --seed 0
"""
import argparse
import copy
import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import build_loaders  # noqa: E402
from src.evaluate import evaluate_model  # noqa: E402
from src.models import build_resnet18  # noqa: E402
from src.pruning.structured import (apply_mask, check_equivalence, mask_hook,  # noqa: E402
                                    physical_prune, select_channels)
from src.train import fit  # noqa: E402
from src.utils import exp_name, get_device, load_config, save_json, set_seed  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--results", default="results")
    ap.add_argument("--max-batches", type=int, default=None, help="so para smoke test")
    ap.add_argument("--epochs", type=int, default=None, help="sobrescreve (so para smoke test)")
    a = ap.parse_args()

    cfg = load_config(a.config)
    sc, hp = cfg["structured"], dict(cfg["finetune"])
    if a.epochs:
        hp["epochs"] = a.epochs
    set_seed(a.seed)
    device = get_device()
    pct = int(sc["ratio"] * 100)
    base = exp_name(1, "baseline", a.seed)
    e5, e6 = exp_name(5, f"struct_mask_{pct}", a.seed), exp_name(6, f"struct_phys_{pct}", a.seed)
    out5, out6 = os.path.join(a.results, e5), os.path.join(a.results, e6)
    os.makedirs(out5, exist_ok=True)
    os.makedirs(out6, exist_ok=True)

    model = build_resnet18(len(cfg["data"]["classes"]), pretrained=False)
    model.load_state_dict(torch.load(os.path.join(a.results, base, f"{base}.pt"), map_location="cpu"))
    example = torch.zeros(1, 3, cfg["data"]["img_size"], cfg["data"]["img_size"])
    loaders = build_loaders(cfg, hp["batch_size"], seed=a.seed)

    # 1) selecao dos canais + mascara
    model.eval()
    plan = select_channels(model, example, ratio=sc["ratio"], ignore=tuple(sc["ignore"]))
    save_json({"seed": a.seed, "ratio": sc["ratio"], "groups": plan},
              os.path.join(out5, f"{e5}_plan.json"))
    apply_mask(model, plan)
    pre = {"exp": e5, "stage": "pre_finetune", **evaluate_model(model, cfg, loaders, device)}
    save_json(pre, os.path.join(out5, f"{e5}_prefinetune_metrics.json"))
    print(f"{e5} antes do fine-tuning: f1_macro={pre['f1_macro']:.4f}")

    # 2) fine-tuning com mascara fixa -> Exp 5
    model, history = fit(model, loaders, hp, device, after_step=mask_hook(plan),
                         max_batches=a.max_batches, log_prefix=f"[{e5}] ")
    apply_mask(model, plan)  # garantia extra
    torch.save(model, os.path.join(out5, f"{e5}_model.pt"))
    save_json({"exp": e5, "hp": hp, "history": history}, os.path.join(out5, f"{e5}_history.json"))
    r5 = {"exp": e5, "stage": "final", **evaluate_model(model, cfg, loaders, device)}
    save_json(r5, os.path.join(out5, f"{e5}_metrics.json"))

    # 3) remocao fisica dos mesmos canais -> Exp 6
    model.cpu().eval()
    phys = physical_prune(copy.deepcopy(model), plan, example)
    eq = check_equivalence(model, phys, torch.randn(4, 3, *example.shape[2:]))
    torch.save(phys, os.path.join(out6, f"{e6}_model.pt"))
    r6 = {"exp": e6, "stage": "final", "equivalence_vs_exp5": eq,
          **evaluate_model(phys, cfg, loaders, device)}
    save_json(r6, os.path.join(out6, f"{e6}_metrics.json"))

    print(f"{e5}: f1_macro={r5['f1_macro']:.4f} params_nonzero={r5['params_nonzero']} "
          f"size_mb={r5['size_mb']:.2f}")
    print(f"{e6}: f1_macro={r6['f1_macro']:.4f} params={r6['params_total']} "
          f"size_mb={r6['size_mb']:.2f} equivalencia={eq}")
    if not eq["equivalent"]:
        raise SystemExit("ERRO: modelo fisico difere do mascarado - investigar antes de usar")


if __name__ == "__main__":
    main()
