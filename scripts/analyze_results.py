"""Comparacao estatistica de cada experimento contra o baseline da mesma semente.

Le results/exp*/<exp>_predictions_test.csv (uma linha por imagem) e calcula, para cada
experimento de poda, a diferenca em relacao ao baseline com intervalo de confianca de
95% por bootstrap PAREADO (as mesmas imagens reamostradas para os dois modelos):
  - F1-macro e acuracia;
  - recall, precisao e F1 de cada classe.
Tambem aplica o teste de McNemar (acertos/erros pareados) na acuracia.

Uma diferenca so e tratada como real quando o intervalo nao contem zero.

Uso:
    python scripts/analyze_results.py --results results --seed 0 [--boot 2000]
Saidas: results/analysis_s<seed>.json e results/analysis_s<seed>.md
"""
import argparse
import csv
import glob
import json
import math
import os
import re

import numpy as np


def load_preds(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["id"]: (r["y_true"], r["y_pred"]) for r in csv.DictReader(fh)}


def per_class(y, p, k):
    cm = np.bincount(y * k + p, minlength=k * k).reshape(k, k)
    tp = np.diag(cm).astype(float)
    sup = cm.sum(1)
    pred = cm.sum(0)
    rec = np.divide(tp, sup, out=np.zeros(k), where=sup > 0)
    prec = np.divide(tp, pred, out=np.zeros(k), where=pred > 0)
    f1 = np.divide(2 * prec * rec, prec + rec, out=np.zeros(k), where=(prec + rec) > 0)
    return rec, prec, f1


def stats(y, p, k):
    rec, prec, f1 = per_class(y, p, k)
    return np.concatenate([[f1.mean(), (y == p).mean()], rec, prec, f1])


def mcnemar(correct_a, correct_b):
    b = int((correct_a & ~correct_b).sum())  # so o baseline acerta
    c = int((~correct_a & correct_b).sum())  # so o experimento acerta
    n = b + c
    if n == 0:
        return {"b": b, "c": c, "p_value": 1.0}
    # teste binomial exato bilateral
    k = min(b, c)
    pv = 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return {"b": b, "c": c, "p_value": min(1.0, pv)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()

    base_name = f"exp1_baseline_s{a.seed}"
    base = load_preds(os.path.join(a.results, base_name, f"{base_name}_predictions_test.csv"))
    ids = sorted(base)
    classes = sorted({t for t, _ in base.values()})
    k = len(classes)
    ci = {c: i for i, c in enumerate(classes)}
    y = np.array([ci[base[i][0]] for i in ids])
    pb = np.array([ci[base[i][1]] for i in ids])
    names = ["f1_macro", "accuracy"] + [f"{m}_{c}" for m in ("recall", "precision", "f1") for c in classes]

    rng = np.random.default_rng(a.seed)
    idx = rng.integers(0, len(ids), size=(a.boot, len(ids)))

    out = {"seed": a.seed, "n_images": len(ids), "boot": a.boot, "baseline": base_name, "experiments": {}}
    md = [f"# Análise estatística — semente {a.seed}", "",
          f"Diferença contra `{base_name}` no teste ({len(ids)} imagens), IC 95% por bootstrap pareado "
          f"({a.boot} reamostragens). `*` = intervalo não contém zero.", ""]
    for path in sorted(glob.glob(os.path.join(a.results, f"exp*_s{a.seed}", f"*_s{a.seed}_predictions_test.csv"))):
        name = re.sub(r"_predictions_test\.csv$", "", os.path.basename(path))
        if name == base_name:
            continue
        pr = load_preds(path)
        if set(pr) != set(ids) or any(pr[i][0] != base[i][0] for i in ids):
            raise SystemExit(f"ERRO: {name} nao tem as mesmas imagens/rotulos do baseline")
        pe = np.array([ci[pr[i][1]] for i in ids])
        point = stats(y, pe, k) - stats(y, pb, k)
        boots = np.array([stats(y[b], pe[b], k) - stats(y[b], pb[b], k) for b in idx])
        lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
        res = {n: {"delta": float(point[j]), "ci95": [float(lo[j]), float(hi[j])],
                   "significativo": bool(lo[j] > 0 or hi[j] < 0)} for j, n in enumerate(names)}
        res["mcnemar_accuracy"] = mcnemar(pb == y, pe == y)
        out["experiments"][name] = res
        md += [f"## {name}", "",
               f"McNemar (acurácia): p = {res['mcnemar_accuracy']['p_value']:.2g} "
               f"(só o baseline acerta: {res['mcnemar_accuracy']['b']}; só o experimento acerta: "
               f"{res['mcnemar_accuracy']['c']})", "",
               "| métrica | Δ (p.p.) | IC 95% |", "|---|---:|---|"]
        for n in ["f1_macro", "accuracy"] + [f"f1_{c}" for c in classes] + [f"recall_{c}" for c in classes]:
            r = res[n]
            md.append(f"| {n} | {100 * r['delta']:+.1f}{' *' if r['significativo'] else ''} | "
                      f"[{100 * r['ci95'][0]:+.1f}, {100 * r['ci95'][1]:+.1f}] |")
        md.append("")

    with open(os.path.join(a.results, f"analysis_s{a.seed}.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(a.results, f"analysis_s{a.seed}.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md[:40]))


if __name__ == "__main__":
    main()
