"""Limpeza e particionamento do MIO-TCD Classification (treino rotulado).

Etapas:
 1. Extrai de cada imagem de train/: md5, pHash, dimensoes (cache em features.tsv,
    retomavel). Le direto do .tar, sem extrair.
 2. Agrupa imagens que sao duplicatas exatas (md5) ou quase-duplicatas (pHash identico)
    via union-find.
 3. Remove grupos com rotulos conflitantes e reduz duplicatas exatas a 1 copia. As demais
    quase-duplicatas ficam, mas o grupo inteiro vai para o mesmo split (evita vazamento).
 4. Por classe, embaralha grupos (semente fixa) e seleciona ate CAP imagens.
 5. Divide os grupos selecionados de cada classe em 70/15/15 (treino/val/teste).
Saida: split.csv (id,classe,split,grupo,largura,altura) e resumo no terminal.

Uso: python scripts/prepare_split.py data/raw/MIO-TCD-Classification.tar [--cache data/interim/features.tsv]
     [--cap 5000] [--seed 42] [--out data/splits/split.csv]
"""
import argparse, collections, hashlib, io, os, random, sys, tarfile

ap = argparse.ArgumentParser()
ap.add_argument('tar'); ap.add_argument('--cache', default='data/interim/features.tsv')
ap.add_argument('--cap', type=int, default=5000); ap.add_argument('--seed', type=int, default=42)
ap.add_argument('--out', default='data/splits/split.csv')
ap.add_argument('--fracs', default='0.70,0.15,0.15')
a = ap.parse_args()
FR = [float(x) for x in a.fracs.split(',')]

# ---------- 1. features (cache retomavel) ----------
def extract():
    from PIL import Image; import imagehash
    done = set()
    if os.path.exists(a.cache):
        done = {l.split('\t', 1)[0] for l in open(a.cache) if l.count('\t') == 6}
    with tarfile.open(a.tar) as t, open(a.cache, 'a') as out:
        for m in t:
            if not (m.isfile() and m.name.startswith('train/') and m.name.endswith('.jpg')) or m.name in done:
                continue
            b = t.extractfile(m).read(); md5 = hashlib.md5(b).hexdigest()
            try:
                im = Image.open(io.BytesIO(b)); im.load()
                out.write(f"{m.name}\t{md5}\t{im.size[0]}\t{im.size[1]}\t{im.mode}\t{imagehash.phash(im.convert('RGB'))}\tNone\n")
            except Exception as e:
                out.write(f"{m.name}\t{md5}\t0\t0\t\tNone\t{str(e)[:50]}\n")
extract()
rows = [l.rstrip('\n').split('\t') for l in open(a.cache) if l.count('\t') == 6]
rows = [r for r in rows if r[6] == 'None']            # descarta corrompidas
print('imagens validas:', len(rows))

# ---------- 2. union-find por md5 e pHash ----------
par = list(range(len(rows)))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
first = {}
for i, r in enumerate(rows):
    for key in ('m' + r[1], 'p' + r[5]):
        if key in first: par[f(i)] = f(first[key])
        else: first[key] = i
groups = collections.defaultdict(list)
for i in range(len(rows)): groups[f(i)].append(i)

# ---------- 3. limpeza ----------
lab = lambda i: rows[i][0].split('/')[1]
clean, n_conf, n_dupe = {}, 0, 0
for g, mem in groups.items():
    if len({lab(i) for i in mem}) > 1: n_conf += len(mem); continue
    seen, keep = set(), []
    for i in sorted(mem, key=lambda i: rows[i][0]):
        if rows[i][1] in seen: n_dupe += 1; continue
        seen.add(rows[i][1]); keep.append(i)
    clean[g] = keep
print('removidas por grupo com rotulo conflitante:', n_conf, '| copias exatas removidas:', n_dupe)

# ---------- 4-5. amostragem com teto + split por grupo ----------
rng = random.Random(a.seed)
bycls = collections.defaultdict(list)
for g, mem in clean.items(): bycls[lab(mem[0])].append(g)
out, summ = [], collections.Counter()
for c in sorted(bycls):
    gs = sorted(bycls[c]); rng.shuffle(gs)
    sel, n = [], 0
    for g in gs:
        if n >= a.cap: break
        sel.append(g); n += len(clean[g])
    cut1, cut2 = FR[0] * n, (FR[0] + FR[1]) * n; acc = 0
    for g in sel:
        sp = 'train' if acc < cut1 else ('val' if acc < cut2 else 'test')
        for i in clean[g]:
            r = rows[i]
            out.append((os.path.basename(r[0])[:-4], c, sp, g, r[2], r[3])); summ[(c, sp)] += 1
        acc += len(clean[g])
with open(a.out, 'w') as fh:
    fh.write('id,classe,split,grupo,largura,altura\n')
    for o in out: fh.write(','.join(map(str, o)) + '\n')
print(f'\n{"classe":22s} {"train":>6s} {"val":>6s} {"test":>6s}')
for c in sorted(bycls):
    print(f'{c:22s} {summ[(c,"train")]:6d} {summ[(c,"val")]:6d} {summ[(c,"test")]:6d}')
print('total', len(out), '->', a.out)
