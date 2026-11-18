"""Correcao das funcoes de deteccao de quase-duplicatas contra calculo ingenuo."""
import numpy as np

from src.dedup import components, hamming_block, min_cross_distance, near_pairs


def _naive(a, b):
    return bin(int(a) ^ int(b)).count("1")


def test_hamming_igual_ao_calculo_ingenuo():
    rng = np.random.default_rng(0)
    a = rng.integers(0, 2**63, size=20, dtype=np.uint64)
    b = rng.integers(0, 2**63, size=30, dtype=np.uint64)
    d = hamming_block(a, b)
    for i in range(20):
        for j in range(30):
            assert d[i, j] == _naive(a[i], b[j])


def test_near_pairs_encontra_todos_os_pares():
    rng = np.random.default_rng(1)
    h = rng.integers(0, 2**63, size=60, dtype=np.uint64)
    h[10] = h[3] ^ np.uint64(0b1011)       # 3 bits
    h[40] = h[3] ^ np.uint64(0xFF)         # 8 bits
    I, J, D = near_pairs(h, 8, chunk=7)
    got = {(int(i), int(j)): int(d) for i, j, d in zip(I, J, D)}
    expected = {(i, j): _naive(h[i], h[j]) for i in range(60) for j in range(i + 1, 60)
                if _naive(h[i], h[j]) <= 8}
    assert got == expected
    assert (3, 10) in got and (3, 40) in got


def test_min_cross_distance():
    a = np.array([0, 0xF], dtype=np.uint64)
    b = np.array([0x1, 0xFF], dtype=np.uint64)
    assert min_cross_distance(a, b).tolist() == [1, 3]


def test_components_transitivos():
    r = components(5, np.array([0, 1]), np.array([1, 2]))
    assert r[0] == r[1] == r[2] and r[3] != r[0] and r[4] != r[3]


def test_entradas_vazias():
    e = np.array([], dtype=np.uint64)
    assert len(min_cross_distance(e, np.array([1], dtype=np.uint64))) == 0
    assert min_cross_distance(np.array([1], dtype=np.uint64), e).tolist() == [65]
    I, J, D = near_pairs(np.array([1], dtype=np.uint64), 8)
    assert len(I) == len(J) == len(D) == 0
