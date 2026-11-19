# Resultados

> **Resultados finais (19/11):** os 6 experimentos nas 3 sementes, com a latência, estão no relatório ([`relatorio/relatorio.pdf`](../relatorio/relatorio.pdf)), em `results/summary.md` e em `results/analysis_s{0,1,2}.md`. Este documento é o registro da **primeira análise**, feita só com os Exp 1, 5 e 6 na semente 0, e foi mantido como histórico.

**Estado (18/11):** Exp 1, 5 e 6 com a semente 0 no **split v2** (Kaggle, T4, notebook versão #3). Os números vêm de `results/summary.md` e `results/analysis_s0.md`, gerados pelos scripts e conferidos contra as predições por imagem (F1 recalculado = JSON; análise refeita localmente = análise do Kaggle).

Teste: 6.869 imagens. IC 95% por bootstrap pareado (2.000 reamostragens). `*` = intervalo não contém zero.

## Visão geral

| Exp | F1-macro | Acurácia | Parâmetros (total / não nulos / efetivos) | Tamanho (MB) | Zip (MB) | MACs (medidos / efetivos) |
|---|---:|---:|---|---:|---:|---|
| 1 — baseline | 0,881 | 0,887 | 11,18 M / 11,18 M / 11,18 M | 42,7 | 39,6 | 485 M / 485 M |
| 5 — estruturado, máscara 50% | 0,837 | 0,844 | 11,18 M / 5,64 M / 2,86 M | 42,7 | 20,1 | 485 M / 176 M |
| 6 — estruturado, físico 50% | 0,837 | 0,844 | 2,86 M / 2,86 M / 2,86 M | 11,0 | 10,2 | 176 M / 176 M |

**Diferença Exp 6 − baseline:** F1-macro **−4,5 p.p.** [−5,3; −3,6] \*; acurácia −4,3 p.p. [−5,1; −3,6] \*; McNemar p = 1,3 × 10⁻²⁵ (561 imagens só o baseline acerta; 263 só o Exp 6).

- **Compressão real só com remoção física.** O Exp 6 tem 26% dos parâmetros, 26% do tamanho e 36% dos MACs do baseline. O Exp 5 tem exatamente as mesmas predições (diferença máxima nas saídas: 2 × 10⁻⁶), mas o arquivo e os MACs medidos não mudam — a economia só aparece no zip e nos valores efetivos.
- **"Não nulos" engana na máscara:** o Exp 5 tem 5,64 M de pesos não nulos, mas só 2,86 M influenciam a saída; o resto lê canais zerados.
- **Sem fine-tuning, a poda destrói o modelo:** F1-macro de 0,039 logo após a poda. A validação durante o fine-tuning (0,777 → 0,834) estabiliza nas últimas épocas.
- O split v2 reduziu o F1 do baseline de 0,896 (split v1, com vazamento) para 0,881: parte do desempenho anterior era memorização de quadros quase iguais.

## Por classe — F1 (baseline → Exp 6)

| Classe | Teste | Baseline | Exp 6 | Δ (p.p.) | IC 95% |
|---|---:|---:|---:|---:|---|
| work_van | 745 | 0,878 | 0,790 | **−8,8 \*** | [−10,8; −6,9] |
| articulated_truck | 743 | 0,862 | 0,790 | −7,2 \* | [−9,5; −5,2] |
| non-motorized_vehicle *(rara)* | 260 | 0,773 | 0,701 | −7,2 \* | [−11,2; −3,0] |
| bicycle *(rara)* | 341 | 0,871 | 0,818 | −5,3 \* | [−8,3; −2,5] |
| car | 747 | 0,863 | 0,811 | −5,2 \* | [−7,3; −3,3] |
| single_unit_truck | 743 | 0,804 | 0,757 | −4,7 \* | [−6,9; −2,6] |
| bus | 749 | 0,951 | 0,915 | −3,5 \* | [−5,0; −2,2] |
| pedestrian | 749 | 0,943 | 0,907 | −3,5 \* | [−5,0; −2,1] |
| motorcycle *(rara)* | 296 | 0,930 | 0,901 | −2,9 \* | [−5,5; −0,3] |
| background | 750 | 0,987 | 0,969 | −1,8 \* | [−2,7; −1,0] |
| pickup_truck | 746 | 0,834 | 0,845 | +1,1 | [−1,1; +3,4] |

## Pergunta central: as classes raras perdem mais?

**Contraste (ΔF1 médio das raras − ΔF1 médio das demais): −0,9 p.p., IC 95% [−3,0; +1,1] — não significativo.** As raras perderam, em média, um pouco mais (−5,1 contra −4,2 p.p.), mas a diferença está dentro do ruído (probabilidade bootstrap de que percam mais: 0,81).

**Leitura:** com a poda estruturada de 50% e 1 semente, **não há evidência de que a frequência da classe determine a perda**. O padrão mais visível é outro — os erros que mais cresceram são entre classes **visualmente parecidas**:

| Confusão | Baseline | Exp 6 |
|---|---:|---:|
| work_van → car | 33 | 75 |
| bus → work_van | 18 | 45 |
| bicycle → pedestrian | 32 | 53 |
| articulated_truck → work_van | 5 | 26 |
| single_unit_truck → articulated_truck | 53 | 71 |

Isso sugere que a poda tira primeiro a capacidade de **distinções finas** (tipos de veículo; bicicleta com ciclista × pedestre — ambiguidade já descrita pelos autores do MIO-TCD). A correlação entre o F1 do baseline e a queda é fraca (0,34), então "classe difícil perde mais" também não é uma regra forte.

## Limitações destes resultados

- 1 semente (D-04): os IC refletem a variação do conjunto de teste, não a do treino. *Resolvido depois: 3 sementes; com elas a queda média do Exp 6 é de 5,3 p.p. e o contraste raras × demais muda de sinal entre sementes.*
- No treino da amostra, o desbalanceamento é ~2,9:1 (não 149:1): o teste da pergunta central tem pouco contraste entre "raras" e "frequentes" por construção.
- Só a poda estruturada. *Resolvido depois: com a L1 (Exp 2–4) a conclusão é a mesma — sem evidência consistente de que as raras percam mais.*
- O `exp5_struct_mask_50_s0_prefinetune_metrics.json` desta execução registra `params_effective`/`macs_effective` iguais aos não nulos (5,64 M / 286 M); o código foi corrigido depois para usar o custo do modelo físico (2,86 M / 176 M). Os demais arquivos já usam o valor certo.

## Histórico: split v1 (descartado)

Com o split v1 (vazamento), o baseline marcava 0,896 e o Exp 5/6 0,821 (5 épocas de fine-tuning) e 0,840 (10 épocas). A primeira leitura ("as raras não sofreram mais") usava só recall, sem intervalos e com vazamento — ver `docs/AUDITORIA_DADOS.md` e o histórico do Git.
