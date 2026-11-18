"""Metricas de custo e poda estruturada em modelos pequenos (CPU, segundos)."""
import copy

import torch
import torch.nn as nn
import torchvision

from src.evaluate import count_macs, count_params, model_size_mb
from src.pruning.structured import (apply_mask, check_equivalence, mask_hook, physical_prune,
                                    select_channels)


class Tiny(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(3, 4, 3, padding=1, bias=False)
        self.fc = nn.Linear(4, 2)

    def forward(self, x):
        return self.fc(self.conv(x).mean((2, 3)))


def test_macs_calculados_a_mao():
    m = Tiny()
    macs = count_macs(m, img_size=8)
    conv = 8 * 8 * 4 * (3 * 3 * 3)
    fc = 4 * 2
    assert macs["macs_measured"] == conv + fc
    with torch.no_grad():
        m.conv.weight[:2] = 0  # metade dos filtros zerada
    assert count_macs(m, img_size=8)["macs_theoretical"] == conv // 2 + fc


def test_contagem_de_parametros_e_esparsidade():
    m = Tiny()
    with torch.no_grad():
        m.conv.weight[:1] = 0
    p = count_params(m)
    assert p["params_total"] == 4 * 27 + 4 * 2 + 2
    assert p["params_nonzero"] == p["params_total"] - 27
    assert abs(p["weight_sparsity"] - 27 / (108 + 8)) < 1e-9


def test_zip_menor_com_zeros():
    m = torchvision.models.resnet18(num_classes=11)
    raw = model_size_mb(m)
    with torch.no_grad():
        for mod in m.modules():
            if isinstance(mod, nn.Conv2d):
                mod.weight.mul_((torch.rand_like(mod.weight) > 0.9).float())
    sparse = model_size_mb(m)
    assert abs(sparse["size_mb"] - raw["size_mb"]) < 0.01      # tamanho puro nao muda
    assert sparse["size_zip_mb"] < 0.5 * raw["size_zip_mb"]     # comprimido diminui


def _resnet():
    torch.manual_seed(0)
    m = torchvision.models.resnet18(num_classes=11)
    for mod in m.modules():
        if isinstance(mod, nn.BatchNorm2d):
            mod.running_mean.uniform_(-0.5, 0.5)
            mod.running_var.uniform_(0.5, 1.5)
            mod.bias.data.uniform_(-0.2, 0.2)
    return m.eval()


def test_plano_respeita_camadas_ignoradas():
    m = _resnet()
    plan = select_channels(m, torch.zeros(1, 3, 112, 112), ratio=0.5, ignore=("conv1", "fc"))
    roots = {g["root"] for g in plan}
    assert "conv1" not in roots and "fc" not in roots
    for g in plan:
        for mem in g["members"]:
            if mem["module"] in ("conv1", "fc"):
                assert mem["handler"] != "prune_out_channels"


def test_mascara_e_fisico_equivalentes():
    m = _resnet()
    ex = torch.randn(4, 3, 112, 112)
    plan = select_channels(m, ex[:1])
    apply_mask(m, plan)
    p = physical_prune(copy.deepcopy(m), plan, ex[:1])
    assert check_equivalence(m, p, ex)["equivalent"]
    n = lambda x: sum(t.numel() for t in x.parameters())  # noqa: E731
    assert 0.70 < 1 - n(p) / n(m) < 0.78


def test_mascara_fixa_no_fine_tuning():
    m = _resnet().train()
    ex = torch.randn(2, 3, 112, 112)
    plan = select_channels(m, ex[:1])
    apply_mask(m, plan)
    opt = torch.optim.SGD(m.parameters(), lr=0.1, momentum=0.9)
    hook = mask_hook(plan)
    for _ in range(2):
        opt.zero_grad()
        m(ex).sum().backward()
        opt.step()
        hook(m)
    named = dict(m.named_modules())
    g = plan[3]
    for mem in g["members"]:
        if mem["handler"] == "prune_out_channels" and isinstance(named[mem["module"]], nn.Conv2d):
            assert named[mem["module"]].weight[mem["idxs"]].abs().sum() == 0
