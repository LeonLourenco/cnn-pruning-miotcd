"""Protege o protocolo contra mudancas acidentais (docs/SPEC.md).

Se um destes testes falhar porque o protocolo mudou DE PROPOSITO, atualize o teste,
docs/SPEC.md e docs/DEMANDAS.md no mesmo commit, explicando o motivo.
"""
import os

from src.utils import load_config


def test_protocolo_default(root):
    cfg = load_config(os.path.join(root, "configs", "default.yaml"))
    assert cfg["data"]["img_size"] == 112
    assert cfg["data"]["split_csv"] == "data/splits/split.csv"
    assert len(cfg["data"]["classes"]) == 11
    assert cfg["model"]["pretrained"] is True
    assert cfg["baseline"]["epochs"] == 20 and cfg["baseline"]["lr"] == 0.01
    assert cfg["finetune"]["epochs"] == 10 and cfg["finetune"]["lr"] == 0.001
    assert cfg["structured"]["ratio"] == 0.5 and cfg["structured"]["ignore"] == ["conv1", "fc"]
    assert cfg["unstructured"]["amounts"] == [0.3, 0.6, 0.9]
    assert cfg["selection_metric"] == "f1_macro"


def test_smoke_espelha_o_protocolo(root):
    d = load_config(os.path.join(root, "configs", "default.yaml"))
    s = load_config(os.path.join(root, "configs", "smoke.yaml"))
    for sec in ("model", "structured", "unstructured"):
        assert d[sec] == s[sec], sec
    for k in ("epochs", "lr", "optimizer", "momentum", "weight_decay", "scheduler"):
        assert d["baseline"][k] == s["baseline"][k] and d["finetune"][k] == s["finetune"][k], k
    assert d["data"]["classes"] == s["data"]["classes"] and d["data"]["img_size"] == s["data"]["img_size"]

def test_unstructured_decidido():
    cfg = load_config("configs/default.yaml")
    assert cfg["unstructured"]["scope"] == "global"
    assert cfg["unstructured"]["ignore"] == ["conv1", "fc"]
