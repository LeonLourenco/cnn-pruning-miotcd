"""Configuracao comum dos testes. Rodar a partir da raiz do repositorio: `python -m pytest`."""
import os
import sys
import tarfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: teste de execucao ponta a ponta (~1-2 min em CPU)")
    config.addinivalue_line("markers", "data: precisa das imagens em data/processed/mio_subset")


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture(scope="session")
def smoke_dir():
    """Extrai data/smoke/smoke.tar (uma vez) e devolve data/smoke/smoke."""
    d = os.path.join(ROOT, "data", "smoke")
    out = os.path.join(d, "smoke")
    if not os.path.exists(os.path.join(out, "split_smoke.csv")):
        with tarfile.open(os.path.join(d, "smoke.tar")) as t:
            try:
                t.extractall(d, filter="data")  # Python >= 3.12: so arquivos comuns
            except TypeError:
                t.extractall(d)
    return out


@pytest.fixture(scope="session")
def split_rows():
    from scripts.audit_data import load_split
    return load_split(os.path.join(ROOT, "data", "splits", "split.csv"))
