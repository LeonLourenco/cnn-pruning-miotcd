"""Benchmark de latencia e throughput dos modelos (docs/SPEC.md, secao "Latencia").

RODAR SOMENTE no notebook do Leon, no Python nativo do Windows (nao em VM, Colab ou Kaggle),
na tomada e com o modo de energia em "Melhor desempenho".

Protocolo:
- numero de threads fixo (torch.set_num_threads);
- modelo em eval() e torch.inference_mode();
- entrada sintetica do tamanho real (a latencia nao depende do conteudo da imagem);
- para cada batch size: aquecimento descartado + medicoes cronometradas;
- as medicoes sao divididas em rodadas, alternando a ordem dos modelos a cada rodada,
  para que o aquecimento do processador nao favoreca nenhum modelo;
- reporta mediana (principal), media, desvio, p95 e throughput (imagens/s).

Uso:
    python scripts/benchmark_latency.py --results results
"""
import argparse
import glob
import json
import os
import platform
import statistics
import sys
import time

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import utf8_stdout, load_config  # noqa: E402


def time_batches(model, x, n):
    times = []
    with torch.inference_mode():
        for _ in range(n):
            t0 = time.perf_counter()
            model(x)
            times.append((time.perf_counter() - t0) * 1000)
    return times


def main():
    utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--results", default="results")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--iters", type=int, default=None, help="sobrescreve (so para teste rapido)")
    ap.add_argument("--warmup", type=int, default=None, help="sobrescreve (so para teste rapido)")
    a = ap.parse_args()

    cfg = load_config(a.config)
    lc = cfg["latency"]
    iters, warmup = a.iters or lc["iters"], a.warmup or lc["warmup"]
    torch.set_num_threads(lc["threads"])
    size = cfg["data"]["img_size"]

    paths = sorted(glob.glob(os.path.join(a.results, "exp*", "*_model.pt")))
    if not paths:
        raise SystemExit(f"nenhum *_model.pt encontrado em {a.results}/exp*/")
    models = {}
    for p in paths:
        m = torch.load(p, map_location="cpu", weights_only=False)
        m.eval()
        models[os.path.basename(p)[:-len("_model.pt")]] = m

    report = {
        "hardware": {"platform": platform.platform(), "processor": platform.processor(),
                     "python": platform.python_version(), "torch": torch.__version__,
                     "threads": lc["threads"]},
        "protocol": {"warmup": warmup, "iters": iters, "rounds": a.rounds},
        "models": {},
    }
    per_round = max(1, iters // a.rounds)
    for bs in lc["batch_sizes"]:
        x = torch.randn(bs, 3, size, size)
        names = list(models)
        for n in names:  # aquecimento de cada modelo
            time_batches(models[n], x, warmup)
        samples = {n: [] for n in names}
        for r in range(a.rounds):
            order = names if r % 2 == 0 else names[::-1]
            for n in order:
                samples[n] += time_batches(models[n], x, per_round)
        for n in names:
            t = samples[n]
            med = statistics.median(t)
            report["models"].setdefault(n, {})[f"batch_{bs}"] = {
                "median_ms": med, "mean_ms": statistics.mean(t), "std_ms": statistics.pstdev(t),
                "p95_ms": sorted(t)[int(0.95 * (len(t) - 1))], "n": len(t),
                "throughput_img_s": bs / (med / 1000),
            }
            print(f"batch={bs:>3} {n:<28} mediana={med:8.2f} ms  "
                  f"throughput={bs / (med / 1000):8.1f} img/s")

    out = os.path.join(a.results, "latency", f"latency_{platform.node() or 'host'}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print("salvo em", out)


if __name__ == "__main__":
    main()
