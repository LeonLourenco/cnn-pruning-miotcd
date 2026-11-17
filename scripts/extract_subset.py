"""Extrai do tar original do MIO-TCD apenas as imagens listadas no split.csv.

Gera a estrutura usada pelo loader (src/data.py):
    <out>/<classe>/<id>.jpg

Uso:
    python scripts/extract_subset.py \
        --tar data/raw/MIO-TCD-Classification.tar \
        --split data/splits/split.csv \
        --out data/processed/mio_subset

Opcional: --limit-per-class-split N extrai so N imagens por (classe, split),
util para gerar um subconjunto minusculo de teste rapido (smoke test).
"""
import argparse
import collections
import csv
import os
import tarfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tar", required=True)
    ap.add_argument("--split", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit-per-class-split", type=int, default=0)
    a = ap.parse_args()

    with open(a.split, newline="") as fh:
        rows = list(csv.DictReader(fh))

    wanted = {}
    count = collections.Counter()
    for r in rows:
        key = (r["classe"], r["split"])
        if a.limit_per_class_split and count[key] >= a.limit_per_class_split:
            continue
        count[key] += 1
        wanted[f"train/{r['classe']}/{r['id']}.jpg"] = r

    os.makedirs(a.out, exist_ok=True)
    done = 0
    with tarfile.open(a.tar) as t:
        for m in t:
            if m.name not in wanted:
                continue
            r = wanted[m.name]
            dst_dir = os.path.join(a.out, r["classe"])
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, f"{r['id']}.jpg")
            done += 1
            # retomavel: pula o que ja foi extraido por uma execucao anterior
            if os.path.exists(dst) and os.path.getsize(dst) == m.size:
                continue
            with open(dst, "wb") as fh:
                fh.write(t.extractfile(m).read())
    print(f"extraidas {done} de {len(wanted)} imagens em {a.out}")
    if done != len(wanted):
        raise SystemExit("ERRO: nem todas as imagens do split foram encontradas no tar")


if __name__ == "__main__":
    main()
