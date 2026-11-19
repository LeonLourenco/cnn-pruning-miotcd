"""Checa a poda L1 sem precisar de dataset. Rode com: python -m pytest tests/ -q"""
import torch
import torch.nn as nn

from src.models import build_resnet18
from src.pruning.unstructured import apply_mask, select_weights

CFG_GLOBAL = {"unstructured": {"scope": "global", "ignore": ["conv1", "fc"]}}
CFG_LAYER = {"unstructured": {"scope": "layer", "ignore": ["conv1", "fc"]}}


def _model():
    torch.manual_seed(0)
    return build_resnet18(11, pretrained=False)


def test_global_zera_a_fracao_pedida_e_respeita_ignore():
    m = _model()
    plan = select_weights(m, 0.6, CFG_GLOBAL)
    apply_mask(m, plan)
    assert "conv1" not in plan and "fc" not in plan
    w = [l.weight for n, l in m.named_modules()
         if isinstance(l, (nn.Conv2d, nn.Linear)) and n not in ("conv1", "fc")]
    zeros = sum(int((t == 0).sum()) for t in w) / sum(t.numel() for t in w)
    assert abs(zeros - 0.6) < 1e-3


def test_layer_zera_a_mesma_fracao_em_cada_camada():
    m = _model()
    plan = select_weights(m, 0.3, CFG_LAYER)
    apply_mask(m, plan)
    for n, l in m.named_modules():
        if isinstance(l, (nn.Conv2d, nn.Linear)) and n not in ("conv1", "fc"):
            assert abs(float((l.weight == 0).float().mean()) - 0.3) < 0.01, n


def test_mascara_nao_some_com_um_passo_de_otimizador():
    m = _model()
    plan = select_weights(m, 0.9, CFG_GLOBAL)
    apply_mask(m, plan)

    w = m.layer1[0].conv1.weight
    dead = plan["layer1.0.conv1"] == 0  # posições que devem ficar em zero

    opt = torch.optim.SGD(m.parameters(), lr=0.1)
    m.train()
    loss = m(torch.randn(4, 3, 64, 64)).sum()
    loss.backward()
    opt.step()

    # sem a máscara, o passo do otimizador reativa pesos podados
    assert (w.detach()[dead] != 0).any()

    # o que mask_hook faz depois de cada passo
    apply_mask(m, plan)
    assert (w.detach()[dead] == 0).all()