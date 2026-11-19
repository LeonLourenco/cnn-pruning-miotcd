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

- [`relatorio/relatorio.pdf`](relatorio/relatorio.pdf) — relatório final (formato SBC)
- [`docs/SPEC.md`](docs/SPEC.md) — protocolo experimental (fonte única de verdade)
- [`docs/DEMANDAS.md`](docs/DEMANDAS.md) — pendências, responsáveis e cronograma
- [`docs/AUDITORIA_DADOS.md`](docs/AUDITORIA_DADOS.md) — escolha da base, limpeza e split
- [`docs/RESULTADOS.md`](docs/RESULTADOS.md) — primeira análise (semente 0, Exp 1, 5 e 6); resultados finais no relatório
- [`docs/EXECUCAO_LOCAL.md`](docs/EXECUCAO_LOCAL.md) — como rodar os Exp 2–4 no próprio computador
- [`docs/KAGGLE.md`](docs/KAGGLE.md) — como treinar no Kaggle (opcional)

## Estrutura

```
configs/      default.yaml (protocolo) e smoke.yaml (teste rápido)
data/splits/  split.csv (v2): partição oficial + relatórios de split e auditoria
data/smoke/   mini-subconjunto (396 imagens) para teste rápido
scripts/      dados (split, auditoria), poda estruturada, latência, consolidação e análise estatística
tests/        integridade dos dados e execução do pipeline (pytest)
src/          dados, modelo, treino, avaliação, poda
results/      saídas por experimento (JSON no Git; .pt fora)
relatorio/    relatório final em PDF e figuras (gerar_figuras.py)
```

## Uso rápido

```bash
pip install -r requirements.txt

# auditoria dos dados e testes (obrigatorios antes de treinar)
python scripts/audit_data.py --img-root data/processed/mio_subset
python -m pytest

# teste de ponta a ponta (CPU, ~1 min)
tar xf data/smoke/smoke.tar -C data/smoke
python -m src.train --config configs/smoke.yaml --epochs 1 --no-pretrained --out-dir /tmp/res
python scripts/run_structured.py --config configs/smoke.yaml --epochs 1 --results /tmp/res

# experimentos reais (GPU, ver docs/KAGGLE.md e docs/EXECUCAO_LOCAL.md), sementes 0, 1 e 2
python -m src.train --seed 0
python scripts/run_structured.py --seed 0
python scripts/run_unstructured.py --seed 0

# latência (só no notebook do Leon, Windows nativo) e consolidação
python scripts/benchmark_latency.py
python scripts/aggregate_results.py
python scripts/analyze_results.py --seed 0   # repetir para 1 e 2
```

## Dados

MIO-TCD Classification — Luo, Z. et al. *MIO-TCD: A New Benchmark Dataset for Vehicle Classification and Localization*. IEEE Transactions on Image Processing, 2018. Licença CC BY-NC-SA 4.0. As imagens não estão no repositório; ver `docs/KAGGLE.md` e `scripts/extract_subset.py`.
