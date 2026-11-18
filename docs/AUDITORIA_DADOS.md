# Auditoria das bases de dados

Resumo do processo de escolha da base (12/11/2026). O feedback do professor pedia trocar o CIFAR-10 por uma base ligada a um problema real.

## Bases avaliadas

| Base | Resultado da auditoria | Decisão |
|---|---|---|
| **MIO-TCD Classification** | Tar íntegro: 648.959 imagens, 0 corrompidas, rótulos 100% consistentes com `gt_train.csv`. Teste oficial **sem rótulos**. Desbalanceamento de 149:1. 1.048 duplicatas exatas; 4% do treino em grupos de quase-duplicatas (pHash idêntico), 200 deles com rótulos conflitantes. | **Escolhida** |
| GTSRB | Íntegra (51.839 imagens), teste oficial rotulado. Treino com 1.307 trilhas de ~30 quadros da mesma placa (vazamento se a validação for aleatória). Acurácia perto do teto (~99%). | Plano B |
| EuroSAT (RGB) | Limpa e balanceada, mas 64×64 px e sem split oficial. | Descartada |
| PlantDoc | 9 imagens idênticas com rótulos diferentes entre treino e teste; classe com 2 imagens; 2,6 mil imagens no total. | Descartada |
| Kaggle "MIO-TCD 50k" | Subconjunto de terceiro sem documentação de amostragem nem licença. | Descartada |
| Kaggle "cardetection" (Roboflow) | Detecção (YOLO), não classificação; ~40% das imagens vêm do GTSRB esticadas para 416 px; vazamento entre splits. | Descartada |

## MIO-TCD: distribuição original do treino

| Classe | Imagens | Lado mediano (px) | % com lado < 64 px |
|---|---:|---:|---:|
| car | 260.518 | 73 | 38% |
| background | 160.000 | 61 | 53% |
| pickup_truck | 50.906 | 83 | 31% |
| articulated_truck | 10.346 | 110 | 26% |
| bus | 10.316 | 184 | 2% |
| work_van | 9.679 | 103 | 15% |
| pedestrian | 6.262 | 49 | 74% |
| single_unit_truck | 5.120 | 124 | 9% |
| bicycle | 2.284 | 70 | 34% |
| motorcycle | 1.982 | 76 | 34% |
| non-motorized_vehicle | 1.751 | 95 | 12% |

Metade das imagens tem lado menor que 72 px → entrada de 112×112 (224 px ampliaria a maioria 3× ou mais).

## Split v1 (12/11) — substituído

`scripts/prepare_split.py`:

1. md5, pHash e dimensões de cada imagem (cache em `data/interim/features.tsv`).
2. Agrupamento por union-find: imagens com md5 igual ou pHash igual ficam no mesmo grupo.
3. Removidas 1.663 imagens de grupos com rótulos conflitantes; duplicatas exatas reduzidas a uma cópia (1.041 removidas).
4. Por classe, grupos embaralhados (semente 42) até o teto de 5.000 imagens.
5. Split 70/15/15 por grupo: um grupo inteiro vai para um único split. Verificado: nenhum grupo em mais de um split.

| Classe | Treino | Val | Teste |
|---|---:|---:|---:|
| 8 classes maiores (cada) | 3.500 | 750 | 750 |
| bicycle | 1.599 | 342 | 342 |
| motorcycle | 1.383 | 296 | 296 |
| non-motorized_vehicle | 1.224 | 262 | 262 |
| **Total** | | | **46.006** |

## Split v2 (18/11) — oficial

**Problema encontrado no v1.** A revisão dos primeiros resultados mediu que 9,3% das imagens de teste tinham uma quase-cópia no treino (pHash a ≤ 4 bits), e 95–97% desses pares eram da mesma classe: quadros quase iguais da mesma câmera. O v1 só agrupava pHash *idêntico*. Isso infla as métricas e pode exagerar a queda da poda (um modelo menor "lembra" menos quadros vistos no treino).

**Escolha do limiar (todas as 46.006 imagens da amostra, todos os pares):**

| Distância pHash (bits) | Pares | Mesma classe | Cruzavam o split v1 |
|---:|---:|---:|---:|
| 0 | 2.776 | 100,0% | 0 |
| 2 | 2.464 | 98,3% | 1.141 |
| 4 | 10.475 | 99,1% | 6.934 |
| 6 | 17.999 | 98,3% | 9.751 |
| 8 | 27.148 | 96,5% | 14.593 |
| 10 | 38.964 | 87,5% | 18.512 |

Até 8 bits, os pares são quase sempre do mesmo objeto. Com 10 bits, o agrupamento transitivo forma um componente único de 9.609 imagens, inviável para o split. **Limiar: 8 bits** (maior grupo resultante: 921 imagens).

**`scripts/regroup_split.py`:**
1. Mesmas 46.006 imagens do v1 (o `mio_subset.zip` não muda).
2. Remove as 218 imagens que têm quase-cópia (≤ 4 bits) com rótulo diferente — 135 pares, provável erro de rótulo.
3. Agrupa quase-duplicatas (≤ 8 bits) por union-find: 3.035 grupos com mais de uma imagem.
4. Distribui grupos inteiros em 70/15/15, de forma estratificada por classe (gulosa, semente 42).
5. Grava `split.csv` com md5 e pHash, para a auditoria rodar só com o Git. Relatório: `data/splits/split_report.json`.

**Resultado:** 45.788 imagens (treino 32.049 · val 6.870 · teste 6.869); maior desvio da proporção 70/15/15 por classe: 0,05 p.p.; menor distância entre imagens de splits diferentes: 10 bits.

**Auditoria independente** (`scripts/audit_data.py`, relatório em `data/splits/audit_report.json`): 10 verificações — esquema, proporções, suporte mínimo no teste, grupos, md5 entre splits, quase-duplicatas entre splits, rótulos conflitantes, existência/integridade/md5 de cada imagem e consistência do mini-subconjunto. Todas passam no v2. **Controle negativo:** o split v1 reprovado na mesma auditoria falha exatamente em S6 (distância mínima entre splits de 2 bits) e S7 (135 conflitos de rótulo).
