"""Gera as figuras do artigo a partir de results/. Rode da raiz do repositorio:

    python relatorio/figuras/gerar_figuras.py
"""
import json
import os
import statistics as st

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(RAIZ, "results")
OUT = os.path.dirname(os.path.abspath(__file__))
SEEDS = (0, 1, 2)
RARAS = {"bicycle", "motorcycle", "non-motorized_vehicle"}
COR = {"comum": "#2a78d6", "rara": "#eb6834"}
TEXTO = "#52514e"


def delta_f1_por_classe(exp):
    """Delta de F1 por classe (exp - baseline da mesma semente), em p.p., para cada semente."""
    d = {}
    for s in SEEDS:
        a = json.load(open(os.path.join(RES, f"analysis_s{s}.json"), encoding="utf-8"))
        e = a["experiments"][f"{exp}_s{s}"]
        for k, v in e.items():
            if k.startswith("f1_") and k != "f1_macro":
                d.setdefault(k[3:], []).append(100 * v["delta"])
    return d


def fig_delta_por_classe():
    d = delta_f1_por_classe("exp6_struct_phys_50")
    ordem = sorted(d, key=lambda c: st.mean(d[c]))  # maior perda em cima
    medias = [st.mean(d[c]) for c in ordem]
    desvios = [st.stdev(d[c]) for c in ordem]
    cores = [COR["rara"] if c in RARAS else COR["comum"] for c in ordem]
    nomes = [c.replace("_", " ") + (" *" if c in RARAS else "") for c in ordem]

    fig, ax = plt.subplots(figsize=(6.0, 3.4), dpi=200)
    y = range(len(ordem))
    ax.barh(y, medias, xerr=desvios, color=cores, height=0.62,
            error_kw={"ecolor": TEXTO, "elinewidth": 1, "capsize": 2})
    ax.set_yticks(list(y))
    ax.set_yticklabels(nomes, fontsize=8, color=TEXTO)
    ax.invert_yaxis()
    ax.axvline(0, color=TEXTO, lw=0.8)
    ax.set_xlabel("ΔF1 da classe, Exp 6 − baseline (p.p.; média ± desvio, 3 sementes)",
                  fontsize=8, color=TEXTO)
    ax.tick_params(axis="x", labelsize=8, colors=TEXTO)
    ax.grid(axis="x", color="#e4e3df", lw=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb6")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=COR["comum"], label="frequente"),
                       Patch(color=COR["rara"], label="rara (*)")],
              fontsize=8, frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "delta_f1_classes.pdf"))
    fig.savefig(os.path.join(OUT, "delta_f1_classes.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_delta_por_classe()
    print("figuras salvas em", OUT)
