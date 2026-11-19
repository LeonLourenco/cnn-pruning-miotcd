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


# ---------------------------------------------------------------------------
# Figuras planejadas na D-11: compressao x F1, latencia x tamanho, recall das
# raras x intensidade. Todas usam media e desvio nas 3 sementes.
# ---------------------------------------------------------------------------
EXPS = [("exp1_baseline", "Denso"), ("exp2_l1_30", "L1 30%"), ("exp3_l1_60", "L1 60%"),
        ("exp4_l1_90", "L1 90%"), ("exp5_struct_mask_50", "Máscara 50%"),
        ("exp6_struct_phys_50", "Física 50%")]
FAMILIA = {"exp1_baseline": "#52514e", "exp2_l1_30": COR["comum"], "exp3_l1_60": COR["comum"],
           "exp4_l1_90": COR["comum"], "exp5_struct_mask_50": COR["rara"],
           "exp6_struct_phys_50": COR["rara"]}
MARCA = {"exp1_baseline": "s", "exp5_struct_mask_50": "D", "exp6_struct_phys_50": "^"}


def metricas(exp):
    return [json.load(open(os.path.join(RES, f"{exp}_s{s}", f"{exp}_s{s}_metrics.json"),
                           encoding="utf-8")) for s in SEEDS]


def latencias():
    lat = {}
    for p in sorted(os.listdir(os.path.join(RES, "latency"))):
        d = json.load(open(os.path.join(RES, "latency", p), encoding="utf-8"))
        for k, v in d["models"].items():
            lat[k.rsplit("_s", 1)[0]] = v
    return lat


def eixo_limpo(ax):
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#bdbcb6")
    ax.tick_params(labelsize=8, colors=TEXTO)
    ax.grid(color="#e4e3df", lw=0.6)
    ax.set_axisbelow(True)


def fig_compressao_f1():
    fig, ax = plt.subplots(figsize=(6.0, 3.4), dpi=200)
    for exp, nome in EXPS:
        m = metricas(exp)
        x = st.mean(r["params_effective"] for r in m) / 1e6
        y = [r["f1_macro"] for r in m]
        ax.errorbar(x, st.mean(y), yerr=st.stdev(y), fmt=MARCA.get(exp, "o"), ms=6,
                    color=FAMILIA[exp], ecolor=TEXTO, elinewidth=1, capsize=2)
        dx, ha = (0.25, "left")
        dy = -0.006 if exp == "exp5_struct_mask_50" else 0.004
        if exp == "exp6_struct_phys_50":
            nome = "Física 50%"
        ax.annotate(nome, (x, st.mean(y)), xytext=(x + dx, st.mean(y) + dy), fontsize=7.5,
                    color=TEXTO, ha=ha)
    ax.set_xlabel("Parâmetros efetivos (milhões)", fontsize=8, color=TEXTO)
    ax.set_ylabel("F1-macro no teste", fontsize=8, color=TEXTO)
    eixo_limpo(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "compressao_f1.png"), dpi=200)
    plt.close(fig)


def fig_latencia_tamanho():
    lat = latencias()
    fig, ax = plt.subplots(figsize=(6.0, 3.2), dpi=200)
    for exp, nome in EXPS:
        x = st.mean(r["size_zip_mb"] for r in metricas(exp))
        y = lat[exp]["batch_1"]["median_ms"]
        ax.plot(x, y, MARCA.get(exp, "o"), ms=6, color=FAMILIA[exp])
        dy = {"exp5_struct_mask_50": -0.55, "exp3_l1_60": 0.3}.get(exp, 0.3)
        ax.annotate(nome, (x, y), xytext=(x + 0.6, y + dy), fontsize=7.5, color=TEXTO)
    ax.set_xlabel("Tamanho do arquivo compactado (MB)", fontsize=8, color=TEXTO)
    ax.set_ylabel("Latência, lote 1 (ms, mediana)", fontsize=8, color=TEXTO)
    ax.set_ylim(0, 14)
    ax.set_xlim(0, 45)
    eixo_limpo(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "latencia_tamanho.png"), dpi=200)
    plt.close(fig)


def fig_recall_raras():
    grupos = [("exp1_baseline", "Denso"), ("exp2_l1_30", "L1 30%"), ("exp3_l1_60", "L1 60%"),
              ("exp4_l1_90", "L1 90%"), ("exp6_struct_phys_50", "Estrut. 50%")]
    series = [("bicycle", "bicycle", COR["comum"], "o"), ("motorcycle", "motorcycle", COR["rara"], "s"),
              ("non-motorized_vehicle", "non-motorized vehicle", "#1baf7a", "^")]
    xs = range(len(grupos))
    fig, ax = plt.subplots(figsize=(6.0, 3.4), dpi=200)
    for cls, rot, cor, mk in series:
        med, dp = [], []
        for exp, _ in grupos:
            v = [r["per_class"][cls]["recall"] for r in metricas(exp)]
            med.append(st.mean(v)); dp.append(st.stdev(v))
        ax.errorbar(xs, med, yerr=dp, fmt="-" + mk, color=cor, ms=5, lw=1.5,
                    ecolor=cor, elinewidth=1, capsize=2, label=rot + " (rara)")
    med = []
    for exp, _ in grupos:
        v = [st.mean(r["per_class"][c]["recall"] for c in r["per_class"] if c not in RARAS)
             for r in metricas(exp)]
        med.append(st.mean(v))
    ax.plot(xs, med, "--", color="#8a8984", lw=1.5, label="demais 8 classes (média)")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([g[1] for g in grupos], fontsize=8, color=TEXTO)
    ax.set_ylabel("Recall no teste", fontsize=8, color=TEXTO)
    ax.legend(fontsize=7.5, frameon=False, loc="lower left")
    eixo_limpo(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "recall_raras.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_delta_por_classe()
    fig_compressao_f1()
    fig_latencia_tamanho()
    fig_recall_raras()
    print("figuras salvas em", OUT)
