"""Split v2: agrupa quase-duplicatas e redistribui treino/val/teste sem vazamento.

Motivo (docs/AUDITORIA_DADOS.md, secao "Split v2"): o split v1 so agrupava pHash
IDENTICO. Quadros quase iguais da mesma camera (distancia de Hamming 2-8 no pHash)
ficavam em splits diferentes: 14.593 pares atravessavam treino/val/teste.

O conjunto de imagens e o MESMO do split v1 (as 46.006 imagens de mio_subset.zip),
menos as que tem quase-copia com rotulo diferente (provavel erro de rotulo).

Etapas:
 1. le split v1 (ids, classes) e features.tsv (md5, pHash, dimensoes);
 2. pares com distancia <= --conflict-dist e classes diferentes -> remove as duas imagens;
 3. pares com distancia <= --dist (limiar 8, escolhido pela analise da secao citada)
    -> union-find -> grupos;
 4. atribuicao estratificada de grupos inteiros a treino/val/teste (gulosa, semente fixa):
    grupos maiores primeiro; cada grupo vai para o split com maior deficit relativo
    das classes que ele contem;
 5. grava o split.csv v2 (com md5 e pHash, para a auditoria rodar so com o Git) e um
    relatorio JSON.

Uso:
    python scripts/regroup_split.py --split-in data/splits/split.csv \
        --features data/interim/features.tsv --out data/splits/split.csv \
        --report data/splits/split_report.json
"""
import argparse
import collections
import csv
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import utf8_stdout  # noqa: E402
from src.dedup import components, hex_to_uint64, min_cross_distance, near_pairs  # noqa: E402

SPLITS = ("train", "val", "test")


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--split-in", required=True)
    ap.add_argument("--features", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--dist", type=int, default=8)
    ap.add_argument("--conflict-dist", type=int, default=4)
    ap.add_argument("--fracs", default="0.70,0.15,0.15")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    fracs = dict(zip(SPLITS, map(float, a.fracs.split(","))))

    with open(a.split_in, newline="") as fh:
        v1 = list(csv.DictReader(fh))
    wanted = {r["id"]: r for r in v1}
    feats = {}
    with open(a.features) as fh:
        for line in fh:
            name, md5, w, h, mode, ph, err = line.rstrip("\n").split("\t")
            _, cls, fname = name.split("/")
            i = fname[:-4]
            if i in wanted:
                feats[i] = {"md5": md5, "phash": ph, "largura": w, "altura": h, "classe_tar": cls}
    missing = [i for i in wanted if i not in feats]
    if missing:
        raise SystemExit(f"ERRO: {len(missing)} ids do split sem features")
    bad_label = [i for i in wanted if feats[i]["classe_tar"] != wanted[i]["classe"]]
    if bad_label:
        raise SystemExit(f"ERRO: {len(bad_label)} ids com classe diferente da pasta original")

    ids = sorted(wanted)
    cls = np.array([wanted[i]["classe"] for i in ids])
    h = hex_to_uint64([feats[i]["phash"] for i in ids])
    I, J, D = near_pairs(h, a.dist)

    # 2) conflitos de rotulo entre quase-copias
    conf = (D <= a.conflict_dist) & (cls[I] != cls[J])
    drop = set(I[conf].tolist()) | set(J[conf].tolist())
    keep = np.array([k not in drop for k in range(len(ids))])

    # 3) grupos so entre as imagens mantidas
    e = keep[I] & keep[J]
    roots = components(len(ids), I[e], J[e])

    # 4) atribuicao estratificada gulosa
    groups = collections.defaultdict(list)
    for k in np.nonzero(keep)[0]:
        groups[roots[k]].append(k)
    class_tot = collections.Counter(cls[keep])
    target = {(s, c): fracs[s] * n for s in SPLITS for c, n in class_tot.items()}
    cur = collections.Counter()
    rng = random.Random(a.seed)
    order = list(groups)
    rng.shuffle(order)                      # desempate aleatorio com semente
    order.sort(key=lambda g: -len(groups[g]))  # sort estavel: maiores primeiro
    assign = {}
    for g in order:
        comp = collections.Counter(cls[groups[g]])
        best, best_score = None, None
        for s in SPLITS:
            score = sum(n * (target[(s, c)] - cur[(s, c)]) / max(target[(s, c)], 1)
                        for c, n in comp.items())
            if best_score is None or score > best_score:
                best, best_score = s, score
        assign[g] = best
        for c, n in comp.items():
            cur[(best, c)] += n

    # 5) saida
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    rows = []
    gid = {g: n for n, g in enumerate(sorted(groups, key=lambda g: min(groups[g])))}
    for k in np.nonzero(keep)[0]:
        i = ids[k]
        rows.append({"id": i, "classe": cls[k], "split": assign[roots[k]], "grupo": gid[roots[k]],
                     "largura": feats[i]["largura"], "altura": feats[i]["altura"],
                     "md5": feats[i]["md5"], "phash": feats[i]["phash"]})
    rows.sort(key=lambda r: (r["classe"], r["split"], r["id"]))
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # verificacao embutida: nenhuma quase-copia entre splits
    spl = np.array([r["split"] for r in rows])
    hh = hex_to_uint64([r["phash"] for r in rows])
    cross = {}
    for s1, s2 in (("train", "val"), ("train", "test"), ("val", "test")):
        cross[f"{s1}-{s2}"] = int(min_cross_distance(hh[spl == s2], hh[spl == s1]).min())
    sizes = sorted((len(v) for v in groups.values()), reverse=True)
    report = {
        "params": vars(a),
        "n_in": len(ids), "n_out": len(rows),
        "removed_label_conflict": sorted(ids[k] for k in drop),
        "pairs_le_dist": int(len(D)), "pairs_conflict": int(conf.sum()),
        "groups": len(groups), "groups_gt1": sum(1 for s in sizes if s > 1),
        "largest_groups": sizes[:10],
        "min_cross_split_distance": cross,
        "counts": {c: {s: int(cur[(s, c)]) for s in SPLITS} for c in sorted(class_tot)},
    }
    with open(a.report, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k not in ("removed_label_conflict", "params")},
                     ensure_ascii=False, indent=1))
    print("removidas por conflito de rotulo:", len(drop))
    if min(cross.values()) <= a.dist:
        raise SystemExit("ERRO: ainda ha quase-copias entre splits")


if __name__ == "__main__":
    main()
