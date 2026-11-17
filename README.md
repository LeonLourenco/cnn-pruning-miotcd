# Pruning em CNNs: classificação de veículos no MIO-TCD

Trabalho da disciplina de Redes Neurais (UFRPE). Avalia como técnicas e intensidades de pruning afetam uma ResNet-18 que classifica veículos em imagens de câmeras de tráfego: tamanho, custo computacional, latência e desempenho preditivo, com atenção às classes raras.

**Autores:** Leon Lourenço · Gabriel Leal

| Exp | Técnica | Intensidade | Responsável |
|---|---|---|---|
| 1 | Modelo denso (baseline) | 0% | Leon |
| 2–4 | L1 não estruturado | 30%, 60%, 90% | Gabriel |
| 5 | Estruturado por canais, máscara | 50% | Leon |
| 6 | Estruturado por canais, remoção física | 50% | Leon |

## Documentação

- [`docs/SPEC.md`](docs/SPEC.md) — protocolo experimental (fonte única de verdade)
- [`docs/DEMANDAS.md`](docs/DEMANDAS.md) — pendências, responsáveis e cronograma
- [`docs/AUDITORIA_DADOS.md`](docs/AUDITORIA_DADOS.md) — escolha da base, limpeza e split
- [`docs/KAGGLE.md`](docs/KAGGLE.md) — como treinar no Kaggle

## Estrutura

```
configs/      default.yaml (protocolo) e smoke.yaml (teste rápido)
data/splits/  split.csv: partição oficial do trabalho
data/smoke/   mini-subconjunto (396 imagens) para teste rápido
scripts/      preparar dados, rodar poda estruturada, latência, consolidar resultados
src/          dados, modelo, treino, avaliação, poda
results/      saídas por experimento (JSON no Git; .pt fora)
```

## Uso rápido

```bash
pip install -r requirements.txt

# teste de ponta a ponta (CPU, ~1 min)
tar xf data/smoke/smoke.tar -C data/smoke
python -m src.train --config configs/smoke.yaml --epochs 1 --no-pretrained --out-dir /tmp/res
python scripts/run_structured.py --config configs/smoke.yaml --epochs 1 --results /tmp/res

# experimentos reais (GPU, ver docs/KAGGLE.md)
python -m src.train --seed 0
python scripts/run_structured.py --seed 0

# latência (só no notebook do Leon, Windows nativo) e consolidação
python scripts/benchmark_latency.py
python scripts/aggregate_results.py
```

## Dados

MIO-TCD Classification — Luo, Z. et al. *MIO-TCD: A New Benchmark Dataset for Vehicle Classification and Localization*. IEEE Transactions on Image Processing, 2018. Licença CC BY-NC-SA 4.0. As imagens não estão no repositório; ver `docs/KAGGLE.md` e `scripts/extract_subset.py`.
