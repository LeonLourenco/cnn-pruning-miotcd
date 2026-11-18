"""Execucao ponta a ponta no mini-subconjunto: baseline -> Exp 5 e 6 -> consolidacao -> analise.

Os numeros nao tem significado (1 epoca, pesos aleatorios); o teste verifica que tudo
executa e que as saidas tem o formato que o restante do pipeline espera.
"""
import csv
import json
import os
import subprocess
import sys

import pytest

KEYS = {"exp", "stage", "split", "n_images", "f1_macro", "accuracy", "per_class", "confusion_matrix",
        "params_total", "params_nonzero", "params_effective", "weight_sparsity", "size_mb",
        "size_zip_mb", "macs_measured", "macs_theoretical", "macs_effective"}


def _run(root, *args):
    r = subprocess.run([sys.executable, *args], cwd=root, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    return r.stdout


@pytest.mark.slow
def test_pipeline_ponta_a_ponta(root, smoke_dir, tmp_path):
    res = str(tmp_path / "results")
    _run(root, "-m", "src.train", "--config", "configs/smoke.yaml", "--epochs", "1",
         "--max-batches", "2", "--no-pretrained", "--out-dir", res)
    _run(root, "scripts/run_structured.py", "--config", "configs/smoke.yaml", "--epochs", "1",
         "--max-batches", "2", "--results", res)

    n_test = 11 * 12
    for exp in ("exp1_baseline_s0", "exp5_struct_mask_50_s0", "exp6_struct_phys_50_s0"):
        with open(os.path.join(res, exp, f"{exp}_metrics.json")) as fh:
            m = json.load(fh)
        assert KEYS <= set(m), KEYS - set(m)
        assert m["n_images"] == n_test
        with open(os.path.join(res, exp, f"{exp}_predictions_test.csv")) as fh:
            assert len(list(csv.DictReader(fh))) == n_test

    with open(os.path.join(res, "exp6_struct_phys_50_s0", "exp6_struct_phys_50_s0_metrics.json")) as fh:
        m6 = json.load(fh)
    with open(os.path.join(res, "exp5_struct_mask_50_s0", "exp5_struct_mask_50_s0_metrics.json")) as fh:
        m5 = json.load(fh)
    assert m6["equivalence_vs_exp5"]["equivalent"]
    assert m5["f1_macro"] == m6["f1_macro"]
    assert m5["params_effective"] == m6["params_total"] < m5["params_total"]
    assert m5["macs_effective"] == m6["macs_measured"] < m5["macs_measured"]
    with open(os.path.join(res, "exp5_struct_mask_50_s0", "exp5_struct_mask_50_s0_prefinetune_metrics.json")) as fh:
        assert json.load(fh)["params_effective"] == m6["params_total"]

    _run(root, "scripts/aggregate_results.py", "--results", res)
    _run(root, "scripts/analyze_results.py", "--results", res, "--boot", "50")
    with open(os.path.join(res, "analysis_s0.json")) as fh:
        a = json.load(fh)
    assert set(a["experiments"]) == {"exp5_struct_mask_50_s0", "exp6_struct_phys_50_s0"}
    assert "contraste_raras_f1" in a["experiments"]["exp6_struct_phys_50_s0"]
    assert a["experiments"]["exp6_struct_phys_50_s0"]["f1_macro"]["delta"] == pytest.approx(
        a["experiments"]["exp5_struct_mask_50_s0"]["f1_macro"]["delta"])
