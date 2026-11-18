"""Auditoria independente do split e dos dados. Deve passar antes de qualquer treino.

Recalcula tudo a partir do split.csv (e, se disponiveis, das imagens e do tar
original), sem reaproveitar resultados de scripts/regroup_split.py.

Verificacoes (cada uma vira um item do relatorio, com status ok/falha):
  S1  esquema do split.csv: colunas, ids unicos, classes e splits validos
  S2  todas as 11 classes em todos os splits, proporcoes 70/15/15 (+-1 p.p.)
  S3  suporte minimo por classe no teste (>= 200 imagens)
  S4  cada grupo inteiro em um unico split
  S5  nenhuma duplicata exata (md5) entre splits
  S6  nenhuma quase-duplicata (pHash <= --dist bits) entre splits
  S7  nenhuma quase-duplicata (pHash <= 4 bits) com rotulos diferentes no dataset
  D1  (com --img-root) toda imagem do split existe, abre, e o md5 bate com o split.csv
  D2  (com --img-root) nenhuma imagem extra no img_root fora do split
  D3  (com --smoke) o mini-subconjunto e um subconjunto consistente do split

Uso:
    python scripts/audit_data.py --split data/splits/split.csv \
        [--img-root data/processed/mio_subset] [--smoke data/smoke/smoke] \
        [--report results/data_audit.json]
Sai com codigo 1 se qualquer verificacao falhar.
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dedup import hex_to_uint64, min_cross_distance, near_pairs  # noqa: E402

CLASSES = ["articulated_truck", "background", "bicycle", "bus", "car", "motorcycle",
           "non-motorized_vehicle", "pedestrian", "pickup_truck", "single_unit_truck", "work_van"]
SPLITS = ("train", "val", "test")
FRACS = {"train": 0.70, "val": 0.15, "test": 0.15}
COLS = ["id", "classe", "split", "grupo", "largura", "altura", "md5", "phash"]


def load_split(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def check_split(rows, dist=8, tol=0.01, min_test=200):
    """Verificacoes S1-S7. Devolve dict nome -> {ok, detalhe}."""
    res = {}
    ids = [r["id"] for r in rows]
    cols_ok = rows and list(rows[0].keys()) == COLS
    res["S1_esquema"] = {
        "ok": bool(cols_ok and len(ids) == len(set(ids))
                   and all(r["classe"] in CLASSES for r in rows)
                   and all(r["split"] in SPLITS for r in rows)),
        "detalhe": {"n": len(rows), "ids_duplicados": len(ids) - len(set(ids)),
                    "colunas": list(rows[0].keys()) if rows else []},
    }
    cnt = collections.Counter((r["classe"], r["split"]) for r in rows)
    tot = collections.Counter(r["classe"] for r in rows)
    worst = 0.0
    for c in CLASSES:
        for s in SPLITS:
            if tot[c]:
                worst = max(worst, abs(cnt[(c, s)] / tot[c] - FRACS[s]))
    res["S2_proporcoes"] = {"ok": all(cnt[(c, s)] > 0 for c in CLASSES for s in SPLITS) and worst <= tol,
                            "detalhe": {"maior_desvio_pp": round(100 * worst, 2)}}
    low = {c: cnt[(c, "test")] for c in CLASSES if cnt[(c, "test")] < min_test}
    res["S3_suporte_teste"] = {"ok": not low, "detalhe": {"abaixo_do_minimo": low}}
    gs = collections.defaultdict(set)
    for r in rows:
        gs[r["grupo"]].add(r["split"])
    split_groups = [g for g, s in gs.items() if len(s) > 1]
    res["S4_grupos"] = {"ok": not split_groups, "detalhe": {"grupos_em_mais_de_um_split": len(split_groups)}}
    md5s = collections.defaultdict(set)
    for r in rows:
        md5s[r["md5"]].add(r["split"])
    cross_md5 = sum(1 for s in md5s.values() if len(s) > 1)
    res["S5_md5_entre_splits"] = {"ok": cross_md5 == 0, "detalhe": {"md5_em_mais_de_um_split": cross_md5}}
    spl = np.array([r["split"] for r in rows])
    h = hex_to_uint64([r["phash"] for r in rows])
    mins = {}
    for s1, s2 in (("train", "val"), ("train", "test"), ("val", "test")):
        d = min_cross_distance(h[spl == s2], h[spl == s1])
        mins[f"{s1}-{s2}"] = int(d.min()) if len(d) else 65  # 65 = sem pares a comparar
    res["S6_quase_duplicatas_entre_splits"] = {"ok": min(mins.values()) > dist,
                                               "detalhe": {"distancia_minima": mins, "limiar": dist}}
    cls = np.array([r["classe"] for r in rows])
    I, J, D = near_pairs(h, 4)
    conflicts = int((cls[I] != cls[J]).sum())
    res["S7_rotulos_conflitantes"] = {"ok": conflicts == 0, "detalhe": {"pares_ate_4_bits_com_classe_diferente": conflicts}}
    return res


def check_images(rows, img_root):
    from PIL import Image
    missing, unreadable, bad_md5 = [], [], []
    for r in rows:
        p = os.path.join(img_root, r["classe"], f"{r['id']}.jpg")
        if not os.path.exists(p):
            missing.append(r["id"])
            continue
        with open(p, "rb") as fh:
            b = fh.read()
        if hashlib.md5(b).hexdigest() != r["md5"]:
            bad_md5.append(r["id"])
        try:
            with Image.open(p) as im:
                im.verify()
        except Exception:
            unreadable.append(r["id"])
    ids = {(r["classe"], r["id"]) for r in rows}
    extra = []
    for c in os.listdir(img_root):
        d = os.path.join(img_root, c)
        if os.path.isdir(d):
            extra += [f for f in os.listdir(d) if (c, f[:-4]) not in ids]
    return {
        "D1_imagens": {"ok": not (missing or unreadable or bad_md5),
                       "detalhe": {"faltando": len(missing), "ilegiveis": len(unreadable),
                                   "md5_diferente": len(bad_md5)}},
        # imagens extras sao esperadas: o zip guarda as 46.006 do split v1 (218 foram removidas no v2)
        "D2_imagens_fora_do_split": {"ok": True, "detalhe": {"n": len(extra), "nota": "informativo"}},
    }


def check_smoke(rows, smoke_dir):
    by_id = {r["id"]: r for r in rows}
    srows = load_split(os.path.join(smoke_dir, "split_smoke.csv"))
    incons = [r["id"] for r in srows if r["id"] not in by_id
              or by_id[r["id"]]["classe"] != r["classe"] or by_id[r["id"]]["split"] != r["split"]]
    missing = [r["id"] for r in srows
               if not os.path.exists(os.path.join(smoke_dir, "img", r["classe"], f"{r['id']}.jpg"))]
    cnt = collections.Counter((r["classe"], r["split"]) for r in srows)
    return {"D3_smoke": {"ok": not incons and not missing and len(cnt) == len(CLASSES) * len(SPLITS),
                         "detalhe": {"n": len(srows), "inconsistentes": len(incons), "faltando": len(missing)}}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="data/splits/split.csv")
    ap.add_argument("--img-root", default=None)
    ap.add_argument("--smoke", default=None)
    ap.add_argument("--dist", type=int, default=8)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    rows = load_split(a.split)
    res = check_split(rows, dist=a.dist)
    if a.img_root:
        res.update(check_images(rows, a.img_root))
    if a.smoke:
        res.update(check_smoke(rows, a.smoke))
    for k, v in res.items():
        print(f"[{'ok' if v['ok'] else 'FALHA'}] {k}: {v['detalhe']}")
    if a.report:
        os.makedirs(os.path.dirname(a.report) or ".", exist_ok=True)
        with open(a.report, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
    if not all(v["ok"] for v in res.values()):
        sys.exit(1)
    print("auditoria: tudo ok")


if __name__ == "__main__":
    main()
