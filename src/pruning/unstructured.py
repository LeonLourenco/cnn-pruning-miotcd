"""Poda nao estruturada L1 (Exp 2, 3 e 4) - RESPONSAVEL: Gabriel.

DEMANDA ABERTA (docs/DEMANDAS.md, D-01): definir antes de implementar
- escopo: global (todas as camadas ordenadas juntas) ou por camada;
- quais camadas ficam fora (sugestao: conv1 e fc, como na poda estruturada);
- registrar a decisao em configs/default.yaml (secao `unstructured`) e em docs/SPEC.md.

Contrato que o restante do pipeline espera (para encaixar em scripts/ e src/evaluate.py):

    plan = select_weights(model, amount, cfg)   # quais pesos zerar
    apply_mask(model, plan)                     # zera os pesos (Exp 2-4)
    fit(model, loaders, cfg["finetune"], device, after_step=mask_hook(plan))
                                                # fine-tuning com mascara FIXA

Cuidados obrigatorios:
- a mascara precisa continuar aplicada durante o fine-tuning (senao os zeros "voltam");
- se usar torch.nn.utils.prune, chamar prune.remove(...) antes de salvar/avaliar:
  sem isso o state_dict guarda weight_orig + weight_mask e o tamanho em MB dobra;
- partir SEMPRE do checkpoint results/exp1_baseline_s<seed>/exp1_baseline_s<seed>.pt
  da mesma semente.
"""

import torch
import torch.nn as nn

SCOPES = ("global", "layer")


def _check_cfg(cfg):
    u = cfg.get("unstructured") or {}
    if u.get("scope") not in SCOPES:
        raise ValueError(f"unstructured.scope precisa ser {SCOPES}, veio {u.get('scope')!r} "
                         "(decisao D-01 ainda em aberto)")
    if u.get("ignore") is None:
        raise ValueError("unstructured.ignore esta null (decisao D-01 ainda em aberto)")
    return u


def _target_layers(model, ignore):
    """Convs e lineares que serao podadas, sem as camadas ignoradas."""
    return [(n, m) for n, m in model.named_modules()
            if isinstance(m, (nn.Conv2d, nn.Linear)) and n not in ignore]


def _keep_mask(scores, n_prune):
    """Vetor float: 1 = mantem, 0 = zera. Zera exatamente os n_prune menores valores."""
    keep = torch.ones(scores.numel(), device=scores.device)
    if n_prune > 0:
        keep[torch.argsort(scores)[:n_prune]] = 0.0
    return keep


@torch.no_grad()
def select_weights(model, amount, cfg):
    """Decide quais pesos zerar. Devolve {nome_da_camada: mascara float com o shape do peso}."""
    u = _check_cfg(cfg)
    layers = _target_layers(model, set(u["ignore"]))
    if not layers:
        raise ValueError("nenhuma camada sobrou para podar: revise unstructured.ignore")

    if u["scope"] == "global":
        scores = torch.cat([m.weight.abs().flatten() for _, m in layers])
        keep = _keep_mask(scores, round(amount * scores.numel()))
        plan, start = {}, 0
        for name, m in layers:  # fatia o vetor global de volta em cada camada
            n = m.weight.numel()
            plan[name] = keep[start:start + n].view_as(m.weight)
            start += n
        return plan

    # scope == "layer": cada camada perde a mesma fracao dos seus proprios pesos
    plan = {}
    for name, m in layers:
        scores = m.weight.abs().flatten()
        keep = _keep_mask(scores, round(amount * scores.numel()))
        plan[name] = keep.view_as(m.weight)
    return plan


@torch.no_grad()
def apply_mask(model, plan):
    """Zera os pesos marcados com 0 no plano."""
    named = dict(model.named_modules())
    for name, keep in plan.items():
        named[name].weight.mul_(keep)


def mask_hook(plan):
    """Funcao para `fit(..., after_step=...)`: reaplica os zeros depois de cada passo."""
    return lambda model: apply_mask(model, plan)


def summarize_plan(plan):
    """Resumo leve para salvar em JSON (a mascara inteira seria grande demais)."""
    layers = {n: {"numel": int(k.numel()), "kept_frac": float(k.mean())}
              for n, k in plan.items()}
    total = sum(v["numel"] for v in layers.values())
    kept = sum(v["kept_frac"] * v["numel"] for v in layers.values())
    return {"layers": layers, "kept_frac_total": kept / total}