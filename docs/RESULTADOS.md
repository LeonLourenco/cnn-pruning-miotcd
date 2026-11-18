# Resultados (parciais)

Gerado a partir de `results/*/*_metrics.json` (semente 0, conjunto de teste, 4.692 imagens). Atualizar quando os Exp 2–4 e a latência entrarem. Tabela completa e sempre atualizada: `results/summary.md` (`scripts/aggregate_results.py`).

**Execução:** Kaggle, GPU T4, versão #2 do notebook (18/11). ~41 s por época.

## Visão geral

| Exp | F1-macro | Acurácia | Parâmetros totais | Não nulos | Tamanho (MB) | Zip (MB) | MACs medidos | MACs teóricos |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 — baseline | 0,896 | 0,902 | 11,18 M | 11,18 M | 42,7 | 39,6 | 485 M | 485 M |
| 5 — estruturado, máscara 50% | 0,840 | 0,846 | 11,18 M | 5,64 M | 42,7 | 20,1 | 485 M | 286 M |
| 6 — estruturado, físico 50% | 0,840 | 0,846 | 2,86 M | 2,86 M | 11,0 | 10,2 | 176 M | 176 M |

- Exp 5 e Exp 6 têm saídas idênticas (diferença máxima 1e-6): a remoção física não muda nada na predição, só no custo.
- O Exp 6 tem 26% dos parâmetros, 26% do tamanho e 36% dos MACs do baseline, por 5,6 pontos de F1-macro.
- Máscara sem remoção física: o arquivo continua com 42,7 MB e os MACs medidos não mudam. A economia só aparece no zip (20,1 MB) e nos MACs teóricos — esparsidade não é aceleração.
- Logo após a poda, antes do fine-tuning, o F1-macro cai para 0,031 (praticamente aleatório): toda a recuperação vem do fine-tuning.

## Fine-tuning: 5 × 10 épocas

| Fine-tuning | F1-macro (teste) | F1 de validação nas últimas épocas |
|---|---:|---|
| 5 épocas (versão #1) | 0,821 | ainda subindo: 0,810 → 0,814 → 0,818 |
| 10 épocas (versão #2, protocolo atual) | 0,840 | estável: 0,833 → 0,831 → 0,833 |

Motivo da mudança em `docs/SPEC.md`, seção 4. O baseline das duas versões é idêntico (F1-macro 0,8961), o que confirma a reprodutibilidade com semente fixa.

## Por classe — recall (baseline → Exp 6)

| Classe | Teste | Baseline | Exp 6 | Variação |
|---|---:|---:|---:|---:|
| articulated_truck | 750 | 0,843 | 0,720 | **−12,3** |
| work_van | 750 | 0,917 | 0,835 | −8,3 |
| car | 750 | 0,901 | 0,821 | −8,0 |
| non-motorized_vehicle *(rara)* | 262 | 0,710 | 0,630 | −8,0 |
| single_unit_truck | 750 | 0,832 | 0,775 | −5,7 |
| bus | 750 | 0,965 | 0,919 | −4,7 |
| pedestrian | 750 | 0,959 | 0,927 | −3,2 |
| bicycle *(rara)* | 342 | 0,863 | 0,833 | −2,9 |
| background | 750 | 0,991 | 0,964 | −2,7 |
| pickup_truck | 750 | 0,871 | 0,851 | −2,0 |
| motorcycle *(rara)* | 296 | 0,970 | 0,953 | −1,7 |

**Leitura preliminar (poda estruturada, 1 semente):** a hipótese de que as classes raras sofrem mais **não se confirma de forma geral**. Bicicleta e moto estão entre as que menos perderam; só "não motorizado" está entre as maiores quedas. As maiores perdas estão nas classes de **veículos parecidos entre si** (caminhão articulado, van, carro, caminhão simples), o que sugere que a poda tira primeiro a capacidade de distinções finas. Com 1 semente, diferenças de 1–2 pontos não são conclusivas. Falta comparar com o L1 (Exp 2–4).
