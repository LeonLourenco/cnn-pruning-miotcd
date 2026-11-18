# Demandas e cronograma

Status: `aberta` · `em andamento` · `feita`. Atualizar este arquivo no mesmo commit que resolve a demanda.

## Cronograma até a apresentação (quinta, 19/11)

| Quando | Leon | Gabriel |
|---|---|---|
| **Ter 17/11** | Base de código pronta e testada (feito); subir dataset no Kaggle; iniciar o baseline (D-05) | Aceitar o convite do repositório; ler `docs/SPEC.md`; decidir D-01 |
| **Qua 18/11 manhã** | Baseline pronto → publicar checkpoint (D-06); rodar Exp 5 e 6 (D-07) | Implementar L1 (D-01) e testar no `configs/smoke.yaml` |
| **Qua 18/11 tarde** | Benchmark de latência dos 6 modelos (D-08) | Rodar Exp 2, 3 e 4 a partir do checkpoint (D-09) |
| **Qua 18/11 noite** | Consolidar resultados (D-10); gráficos (D-11) | Revisar resultados e análise |
| **Qui 19/11** | Slides e ensaio (D-12) | Slides e ensaio (D-12) |

Se o tempo apertar, a ordem de corte é: sementes extras (D-04) → gráficos além da tabela (D-11).

**Atenção (18/11):** o fine-tuning agora é de **10 épocas** para todos os experimentos de poda (`configs/default.yaml`). O Gabriel deve partir do repositório atualizado.

## Demandas

| ID | Demanda | Responsável | Status | Depende de |
|---|---|---|---|---|
| D-01 | **Definir e implementar a poda L1 não estruturada**: escopo global ou por camada; camadas excluídas; registrar em `configs/default.yaml` e `docs/SPEC.md` (seção 6); implementar `src/pruning/unstructured.py` seguindo o contrato do arquivo | Gabriel | aberta | — |
| D-02 | Informar o modelo da GPU do desktop do Gabriel e a versão do PyTorch usada | Gabriel | aberta | — |
| D-03 | **Fechar o protocolo de latência**: confirmar 4 threads, batch 1 e 32, entrada sintética, mediana como valor principal; decidir se mede memória (RAM de pico) | Leon + Gabriel | aberta (em discussão) | — |
| D-04 | Rodar sementes 1 e 2 em todos os experimentos (média ± desvio) | Ambos | aberta (opcional, se houver tempo) | D-09 |
| D-06 | Anexar à Release `dados-baseline-s0` o `exp1_baseline_s0.pt` e o `mio_subset.zip` (guia: `docs/EXECUCAO_LOCAL.md`) | Leon | em andamento | — |
| D-08 | Benchmark de latência dos 6 modelos no notebook do Leon (Windows nativo) | Leon | aberta | D-03, D-09 |
| D-09 | Rodar Exp 2, 3 e 4 no próprio computador (o notebook do Kaggle é opcional) | Gabriel | aberta | D-01, D-06 |
| D-10 | `scripts/aggregate_results.py` com todos os resultados | Leon | aberta | D-08 |
| D-11 | Gráficos: compressão × F1-macro; recall das classes raras × intensidade de poda; latência × tamanho | Ambos | aberta | D-10 |
| D-12 | Slides: problema e base, auditoria dos dados, metodologia, resultados, limitações, conclusão | Ambos | aberta | D-10 |

## Feitas

| ID | Demanda | Quando |
|---|---|---|
| F-01 | Escolha e auditoria das bases (MIO-TCD escolhida) | 12/11 |
| F-02 | Limpeza, amostra e split sem vazamento (`split.csv`) | 12/11 |
| F-03 | Repositório privado no GitHub + convite ao Gabriel | 17/11 |
| F-04 | Base de código: dados, treino, avaliação, poda estruturada, latência, agregação | 17/11 |
| F-05 | Teste de ponta a ponta no mini-subconjunto (`configs/smoke.yaml`): máscara e físico com saídas idênticas | 17/11 |
| F-06 | Dataset privado `leonloureno/mio-tcd-subset-46k` no Kaggle + notebook `notebooks/kaggle_pipeline.ipynb` (antiga D-05) | 18/11 |
| F-07 | Exp 1 com semente 0 no Kaggle (T4). Teste: baseline F1-macro 0,896 (antiga D-05) | 18/11 |
| F-08 | Protocolo: fine-tuning de 5 para 10 épocas, porque o F1 de validação do Exp 5 ainda subia na 5ª época (motivo em `docs/SPEC.md`, seção 4). Exp 5 e 6 rodados de novo com 10 épocas | 18/11 |
| F-09 | Resultados do Exp 1, 5 e 6 (semente 0) no repositório: F1-macro 0,896 (baseline) e 0,840 (Exp 5 e 6, fine-tuning de 10 épocas). Análise em `docs/RESULTADOS.md` | 18/11 |
