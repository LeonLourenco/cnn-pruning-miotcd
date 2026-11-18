"""Treino do baseline (Exp 1) e laco de treino reutilizado no fine-tuning (Exp 2-6).

Uso (baseline):
    python -m src.train --config configs/default.yaml --seed 0

Saidas em results/<exp>/:
    <exp>.pt           state_dict do melhor checkpoint (melhor F1-macro na validacao)
    <exp>_history.json metricas por epoca
"""
import argparse
import copy
import os
import time

import torch
import torch.nn as nn
from sklearn.metrics import f1_score

from src.data import build_loaders
from src.models import build_resnet18
from src.utils import utf8_stdout, exp_name, get_device, load_config, save_json, set_seed


def make_optimizer(model, hp):
    if hp["optimizer"] != "sgd":
        raise ValueError("protocolo usa SGD")
    return torch.optim.SGD(model.parameters(), lr=hp["lr"], momentum=hp["momentum"],
                           weight_decay=hp["weight_decay"])


@torch.no_grad()
def predict(model, loader, device):
    model.eval()
    ys, ps = [], []
    for x, y in loader:
        out = model(x.to(device, non_blocking=True))
        ps.append(out.argmax(1).cpu())
        ys.append(y)
    return torch.cat(ys).numpy(), torch.cat(ps).numpy()


def fit(model, loaders, hp, device, after_step=None, max_batches=None, log_prefix=""):
    """Treina por hp['epochs'] epocas e devolve (melhor_modelo, historico).

    after_step: funcao chamada apos cada passo do otimizador. A poda usa isso
                para manter os pesos podados em zero durante o fine-tuning.
    max_batches: limita lotes por epoca (so para o teste rapido / smoke test).
    """
    model.to(device)
    opt = make_optimizer(model, hp)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=hp["epochs"])
    loss_fn = nn.CrossEntropyLoss()  # sem pesos por classe (decisao do protocolo)
    best_f1, best_state, history = -1.0, None, []

    for epoch in range(1, hp["epochs"] + 1):
        model.train()
        t0, tot_loss, n = time.time(), 0.0, 0
        for b, (x, y) in enumerate(loaders["train"]):
            if max_batches and b >= max_batches:
                break
            x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
            opt.zero_grad(set_to_none=True)
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
            if after_step:
                after_step(model)
            tot_loss += loss.item() * len(y)
            n += len(y)
        sched.step()

        yv, pv = predict(model, loaders["val"], device)
        f1 = f1_score(yv, pv, average="macro")
        acc = float((yv == pv).mean())
        history.append({"epoch": epoch, "train_loss": tot_loss / max(n, 1), "val_f1_macro": f1,
                        "val_acc": acc, "lr": sched.get_last_lr()[0], "secs": time.time() - t0})
        print(f"{log_prefix}epoca {epoch}/{hp['epochs']} loss={tot_loss / max(n, 1):.4f} "
              f"val_f1_macro={f1:.4f} val_acc={acc:.4f} ({time.time() - t0:.0f}s)", flush=True)
        if f1 > best_f1:
            best_f1, best_state = f1, copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    return model, history


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser(description="Treina o baseline denso (Exp 1)")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--max-batches", type=int, default=None, help="so para smoke test")
    ap.add_argument("--epochs", type=int, default=None, help="sobrescreve (so para smoke test)")
    ap.add_argument("--no-pretrained", action="store_true", help="so para smoke test sem internet")
    a = ap.parse_args()

    cfg = load_config(a.config)
    hp = dict(cfg["baseline"])
    if a.epochs:
        hp["epochs"] = a.epochs
    set_seed(a.seed)
    device = get_device()
    name = exp_name(1, "baseline", a.seed)
    out = os.path.join(a.out_dir, name)

    loaders = build_loaders(cfg, hp["batch_size"], seed=a.seed)
    model = build_resnet18(len(cfg["data"]["classes"]),
                           pretrained=cfg["model"]["pretrained"] and not a.no_pretrained)
    model, history = fit(model, loaders, hp, device, max_batches=a.max_batches)

    os.makedirs(out, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(out, f"{name}.pt"))      # ponto de partida da poda
    torch.save(model, os.path.join(out, f"{name}_model.pt"))             # modelo inteiro p/ latencia
    save_json({"exp": name, "seed": a.seed, "hp": hp, "device": str(device), "history": history},
              os.path.join(out, f"{name}_history.json"))

    from src.evaluate import evaluate_model  # import local evita ciclo de imports
    res = {"exp": name, "stage": "final",
           **evaluate_model(model, cfg, loaders, device,
                            pred_path=os.path.join(out, f"{name}_predictions_test.csv"))}
    save_json(res, os.path.join(out, f"{name}_metrics.json"))
    print(f"{name}: test f1_macro={res['f1_macro']:.4f} acc={res['accuracy']:.4f}")
    print("checkpoint salvo em", os.path.join(out, f"{name}.pt"))


if __name__ == "__main__":
    main()
