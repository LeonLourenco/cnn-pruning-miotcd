"""Integridade do split oficial (roda so com o Git, sem as imagens) + controles negativos."""
import collections
import copy

import pytest

from scripts.audit_data import CLASSES, check_split


def test_split_oficial_passa_em_todas_as_verificacoes(split_rows):
    res = check_split(split_rows, dist=8)
    falhas = {k: v["detalhe"] for k, v in res.items() if not v["ok"]}
    assert not falhas, falhas


def test_tamanho_e_classes_do_split(split_rows):
    cnt = collections.Counter(r["split"] for r in split_rows)
    assert len(split_rows) == 45788
    assert set(r["classe"] for r in split_rows) == set(CLASSES)
    assert cnt["test"] == sum(1 for r in split_rows if r["split"] == "test") > 6000


def _two_rows(phash_a, phash_b, cls_a="car", cls_b="car", split_a="train", split_b="test",
              grupo_a="1", grupo_b="2", md5_a="a", md5_b="b"):
    base = {"largura": "64", "altura": "64"}
    return [dict(base, id="1", classe=cls_a, split=split_a, grupo=grupo_a, md5=md5_a, phash=phash_a),
            dict(base, id="2", classe=cls_b, split=split_b, grupo=grupo_b, md5=md5_b, phash=phash_b)]


# Controles negativos: a auditoria precisa FALHAR quando o problema existe.

def test_detecta_quase_duplicata_entre_splits():
    rows = _two_rows("ffffffffffffffff", "fffffffffffffff0")  # 4 bits de diferenca
    assert not check_split(rows, dist=8)["S6_quase_duplicatas_entre_splits"]["ok"]


def test_aceita_imagens_distantes_entre_splits():
    rows = _two_rows("ffffffffffffffff", "0000000000000000")
    assert check_split(rows, dist=8)["S6_quase_duplicatas_entre_splits"]["ok"]


def test_detecta_rotulo_conflitante():
    rows = _two_rows("ffffffffffffffff", "fffffffffffffffe", cls_b="bus", split_b="train")
    assert not check_split(rows, dist=8)["S7_rotulos_conflitantes"]["ok"]


def test_detecta_grupo_dividido():
    rows = _two_rows("ffffffffffffffff", "0000000000000000", grupo_b="1")
    assert not check_split(rows, dist=8)["S4_grupos"]["ok"]


def test_detecta_md5_entre_splits():
    rows = _two_rows("ffffffffffffffff", "0000000000000000", md5_b="a")
    assert not check_split(rows, dist=8)["S5_md5_entre_splits"]["ok"]


def test_detecta_id_duplicado(split_rows):
    rows = copy.deepcopy(split_rows[:5]) + copy.deepcopy(split_rows[:1])
    assert not check_split(rows, dist=8)["S1_esquema"]["ok"]


@pytest.mark.data
def test_imagens_existem_e_batem_com_md5(split_rows, root):
    import os
    from scripts.audit_data import check_images
    img_root = os.path.join(root, "data", "processed", "mio_subset")
    if not os.path.isdir(img_root):
        pytest.skip("imagens nao extraidas em data/processed/mio_subset")
    res = check_images(split_rows, img_root)
    assert res["D1_imagens"]["ok"], res["D1_imagens"]["detalhe"]


def test_smoke_consistente_com_split(split_rows, smoke_dir):
    from scripts.audit_data import check_smoke
    res = check_smoke(split_rows, smoke_dir)
    assert res["D3_smoke"]["ok"], res["D3_smoke"]["detalhe"]
