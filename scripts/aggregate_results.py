"""Junta todos os JSONs de resultados numa tabela unica (sem copiar numeros a mao).

Le results/exp*/*_metrics.json (+ *_prefinetune_metrics.json) e, se existir,
results/latency/latency_*.json. Escreve results/summary.csv e results/summary.md.

Com mais de uma semente, as metricas sao agregadas por experimento (media e desvio).

Uso:
    python scripts/aggregate_results.py --results results
"""
import argparse
import csv
import glob
import json
import os
import re
import statistics

COLS = ["f1_macro", "accuracy", "n_images", "params_total", "params_nonzero", "params_effective", "weight_sparsity",
        "size_mb", "size_zip_mb", "macs_measured", "macs_theoretical", "macs_effective"]
RARE = ["bicycle", "motorcycle", "non-motorized_vehicle"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results")
    a = ap.parse_args()

    lat = {}
    for p in glob.glob(os.path.join(a.results, "latency", "latency_*.json")):
        with open(p, encoding="utf-8") as fh:
            for name, v in json.load(fh)["models"].items():
                lat[name] = v

    rows = []
    for p in sorted(glob.glob(os.path.join(a.results, "exp*", "*metrics.json"))):
        with open(p, encoding="utf-8") as fh:
            r = json.load(fh)
        row = {"exp": r["exp"], "stage": r.get("stage", "final")}
        row.update({c: r.get(c) for c in COLS})
        for c in RARE:
            row[f"recall_{c}"] = r["per_class"][c]["recall"]
        if row["stage"] == "final" and r["exp"] in lat:
            for bs, v in lat[r["exp"]].items():
                row[f"latency_{bs}_median_ms"] = v["median_ms"]
                row[f"throughput_{bs}_img_s"] = v["throughput_img_s"]
        rows.append(row)
    if not rows:
        raise SystemExit("nenhum *_metrics.json encontrado")

    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("exp", "stage"), k))
    with open(os.path.join(a.results, "summary.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # agregacao por experimento (remove o sufixo _s<semente>)
    groups = {}
    for r in rows:
        key = (re.sub(r"_s\d+$", "", r["exp"]), r["stage"])
        groups.setdefault(key, []).append(r)
    show = ["f1_macro", "params_effective", "size_mb", "macs_effective",
            "recall_bicycle", "recall_motorcycle", "latency_batch_1_median_ms"]
    lines = ["| experimento | etapa | n | " + " | ".join(show) + " |",
             "|---|---|---|" + "---|" * len(show)]
    for (exp, stage), rs in sorted(groups.items()):
        cells = []
        for c in show:
            vals = [r[c] for r in rs if r.get(c) is not None]
            if not vals:
                cells.append("-")
            elif len(vals) == 1:
                cells.append(f"{vals[0]:.4g}")
            else:
                cells.append(f"{statistics.mean(vals):.4g} ± {statistics.stdev(vals):.2g}")
        lines.append(f"| {exp} | {stage} | {len(rs)} | " + " | ".join(cells) + " |")
    with open(os.path.join(a.results, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
