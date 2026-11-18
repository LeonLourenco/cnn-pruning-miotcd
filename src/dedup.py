"""Deteccao de quase-duplicatas por pHash (64 bits) e agrupamento por union-find.

Usado por scripts/regroup_split.py (gera o split) e por scripts/audit_data.py e
tests/ (verificam o split de forma independente). Sem dependencia de PyTorch.
"""
import numpy as np

_POPCOUNT = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)


def hex_to_uint64(hexes):
    return np.array([int(h, 16) for h in hexes], dtype=np.uint64)


def hamming_block(a, b):
    """Distancias de Hamming entre todos os pares de a (n) e b (m) -> matriz n x m (uint8)."""
    x = np.bitwise_xor(a[:, None], b[None, :])
    return _POPCOUNT[x.view(np.uint8)].reshape(len(a), len(b), 8).sum(2, dtype=np.uint8)


def near_pairs(h, max_dist, chunk=1000):
    """Todos os pares (i < j) com distancia de Hamming <= max_dist. Devolve (I, J, D)."""
    n = len(h)
    if n < 2:
        e = np.array([], dtype=np.int64)
        return e, e, np.array([], dtype=np.uint8)
    I, J, D = [], [], []
    for a in range(0, n, chunk):
        d = hamming_block(h[a:a + chunk], h)
        r, c = np.nonzero(d <= max_dist)
        r = r + a
        keep = c > r
        I.append(r[keep])
        J.append(c[keep])
        D.append(d[r[keep] - a, c[keep]])
    return np.concatenate(I), np.concatenate(J), np.concatenate(D)


def min_cross_distance(h_a, h_b, chunk=1000):
    """Para cada item de h_a, a menor distancia ate qualquer item de h_b."""
    if len(h_a) == 0 or len(h_b) == 0:
        return np.full(len(h_a), 65, dtype=np.uint8)  # sem vizinhos: maior que 64 bits
    out = []
    for a in range(0, len(h_a), chunk):
        out.append(hamming_block(h_a[a:a + chunk], h_b).min(1))
    return np.concatenate(out)


def components(n, I, J):
    """Componentes conexos (union-find) dado o conjunto de arestas (I, J)."""
    parent = np.arange(n)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in zip(I.tolist(), J.tolist()):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return np.array([find(x) for x in range(n)])
