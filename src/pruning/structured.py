"""Poda estruturada por canais (Exp 5 com mascara, Exp 6 com remocao fisica).

Desenho (docs/SPEC.md, secao "Poda estruturada"):
1. `select_channels` escolhe, em cada grupo de dependencia, 50% dos canais com menor
   norma L1 dos filtros. Os grupos vem do torch-pruning (DepGraph), que junta os canais
   ligados pelas conexoes residuais da ResNet. conv1 e fc ficam fora.
2. `apply_mask` zera esses canais SEM mudar o formato dos tensores (Exp 5): zera os
   filtros da conv e o gamma/beta do BatchNorm, entao a saida desses canais e 0.
   `mask_hook` reaplica os zeros apos cada passo do otimizador no fine-tuning.
3. `physical_prune` remove fisicamente OS MESMOS canais do modelo ja ajustado (Exp 6).
   Como os canais removidos so produziam zeros, a saida do modelo nao muda:
   `check_equivalence` confirma isso numericamente.
"""
import torch
import torch.nn as nn
import torch_pruning as tp


def _names(model):
    return {m: n for n, m in model.named_modules()}


def select_channels(model, example_inputs, ratio=0.5, ignore=("conv1", "fc")):
    """Devolve o plano de poda: lista de grupos, cada um com a camada raiz,
    os indices dos canais e todas as camadas afetadas (com seus indices)."""
    named = dict(model.named_modules())
    ignored = [named[n] for n in ignore]
    names = _names(model)
    pruner = tp.pruner.MetaPruner(
        model, example_inputs,
        importance=tp.importance.MagnitudeImportance(p=1),  # norma L1
        pruning_ratio=ratio, ignored_layers=ignored, global_pruning=False,
    )
    plan = []
    for group in pruner.step(interactive=True):  # interativo: so le, nao poda
        root = group[0]
        members = []
        for dep, idxs in group:
            mod = dep.target.module
            if mod in names and isinstance(mod, (nn.Conv2d, nn.BatchNorm2d, nn.Linear)):
                members.append({"module": names[mod], "handler": dep.handler.__name__,
                                "idxs": [int(i) for i in idxs]})
        plan.append({"root": names[root.dep.target.module],
                     "root_type": type(root.dep.target.module).__name__,
                     "idxs": [int(i) for i in root.idxs], "members": members})
    return plan


@torch.no_grad()
def apply_mask(model, plan):
    """Zera a saida dos canais selecionados (Exp 5). Mantem o formato dos tensores."""
    named = dict(model.named_modules())
    for g in plan:
        for m in g["members"]:
            if m["handler"] != "prune_out_channels":
                continue
            mod, idx = named[m["module"]], torch.tensor(m["idxs"], dtype=torch.long)
            if isinstance(mod, nn.Conv2d):
                mod.weight[idx] = 0
                if mod.bias is not None:
                    mod.bias[idx] = 0
            elif isinstance(mod, nn.BatchNorm2d):
                mod.weight[idx] = 0
                mod.bias[idx] = 0


def mask_hook(plan):
    """Funcao para `fit(..., after_step=...)`: mantem os canais zerados no fine-tuning."""
    return lambda model: apply_mask(model, plan)


def physical_prune(model, plan, example_inputs):
    """Remove fisicamente os mesmos canais do plano (Exp 6). Altera o modelo no lugar."""
    named = dict(model.named_modules())
    dg = tp.DependencyGraph().build_dependency(model, example_inputs=example_inputs)
    fn = {"Conv2d": tp.prune_conv_out_channels, "BatchNorm2d": tp.prune_batchnorm_out_channels}
    for g in plan:
        group = dg.get_pruning_group(named[g["root"]], fn[g["root_type"]], idxs=g["idxs"])
        group.prune()
    return model


@torch.no_grad()
def check_equivalence(masked, physical, example_inputs, atol=1e-4):
    """Compara as saidas do modelo mascarado e do fisico na mesma entrada."""
    masked.eval()
    physical.eval()
    diff = (masked(example_inputs) - physical(example_inputs)).abs().max().item()
    return {"max_abs_diff": diff, "equivalent": diff <= atol}
